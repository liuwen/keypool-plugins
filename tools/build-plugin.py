#!/usr/bin/env python3
"""Export the canonical KeyPool plugin, Agents API, or private ChatGPT variant.

The canonical package remains in plugins/keypool. This script only writes to
ignored dist directories and never reads credential values.
"""

import argparse
import json
import os
from pathlib import Path
import re
import stat
import sys
from urllib.parse import urlsplit
import zipfile


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "plugins" / "keypool"
DESTINATION = ROOT / "dist" / "keypool-plugin"
SOURCE_FILES = (
    "plugin.json",
    "mcp.json",
    "assets/icon.png",
    "skills/keypool/SKILL.md",
    "skills/keypool/agents/openai.yaml",
    "skills/keypool/references/data.md",
    "skills/keypool/references/media.md",
    "skills/keypool/references/search.md",
)
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def require_real_directory(path: Path) -> None:
    if path.is_symlink() or not path.is_dir():
        raise ValueError(f"Expected a real directory: {path}")


def require_regular_file(path: Path) -> None:
    if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode):
        raise ValueError(f"Expected a regular file without symlinks: {path}")


def read_source(relative: str) -> bytes:
    path = SOURCE
    require_real_directory(path)
    for component in Path(relative).parts[:-1]:
        path = path / component
        require_real_directory(path)
    path = path / Path(relative).name
    require_regular_file(path)
    if not path.resolve().is_relative_to(SOURCE.resolve()):
        raise ValueError(f"Source path escapes plugin root: {relative}")
    return path.read_bytes()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def assert_allowed_tree(root: Path, allowed_files: set[str]) -> None:
    """Reject unexpected files and all symlinks in a source or output tree."""
    require_real_directory(root)
    allowed_dirs = {
        parent.as_posix()
        for name in allowed_files
        for parent in Path(name).parents
        if parent != Path(".")
    }
    for current, dirs, files in os.walk(root, followlinks=False):
        base = Path(current)
        for name in dirs:
            path = base / name
            require_real_directory(path)
            if path.relative_to(root).as_posix() not in allowed_dirs:
                raise ValueError(f"Unexpected directory in plugin package: {path}")
        for name in files:
            path = base / name
            require_regular_file(path)
            relative = path.relative_to(root).as_posix()
            if relative not in allowed_files:
                raise ValueError(f"Unexpected file in plugin package: {path}")


def prepare_output(destination: Path, package_name: str, payloads: dict[str, bytes]) -> Path:
    dist = ROOT / "dist"
    if dist.exists() or dist.is_symlink():
        require_real_directory(dist)
    else:
        dist.mkdir()
    if destination.exists() or destination.is_symlink():
        require_real_directory(destination)
        allowed = {f"{package_name}.zip", *(f"{package_name}/{name}" for name in payloads)}
        assert_allowed_tree(destination, allowed)
    else:
        destination.mkdir()
    package = destination / package_name
    if package.exists() or package.is_symlink():
        require_real_directory(package)
    else:
        package.mkdir()
    return package


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("agents-api", "public"), default="agents-api")
    parser.add_argument(
        "--chatgpt-app-id",
        help="Verified registered app ID; builds a private ChatGPT web package",
    )
    parser.add_argument("--chatgpt-base-archive", type=Path,
                        help="Fresh ZIP downloaded from the existing cloud plugin")
    parser.add_argument("--chatgpt-package-name", help="Verified cloud plugin package name")
    parser.add_argument("--chatgpt-version", help="Next cloud plugin version, independent of the backend")
    args = parser.parse_args()
    cloud_options = (args.chatgpt_base_archive, args.chatgpt_package_name, args.chatgpt_version)
    if any(cloud_options) and not (all(cloud_options) and args.chatgpt_app_id):
        parser.error("Cloud updates require base archive, package name, version and app ID")
    if args.chatgpt_app_id and args.target != "agents-api":
        parser.error("--chatgpt-app-id cannot be combined with --target public")
    if args.chatgpt_app_id and not re.fullmatch(
        r"(?:asdk_app_|connector_|templated_apps_)[A-Za-z0-9_-]+", args.chatgpt_app_id
    ):
        raise ValueError("Expected an app ID, without a plugin_ prefix or URL")

    require_real_directory(ROOT / "plugins")
    assert_allowed_tree(SOURCE, set(SOURCE_FILES))
    payloads = {name: read_source(name) for name in SOURCE_FILES}
    manifest = json.loads(payloads["plugin.json"])
    if not isinstance(manifest, dict) or manifest.get("name") != "keypool" or not all(
        isinstance(manifest.get(field), str) and manifest[field]
        for field in ("version", "description")
    ):
        raise ValueError("Unexpected portable plugin identity")

    mcp = json.loads(payloads["mcp.json"])
    if not isinstance(mcp, dict):
        raise ValueError("Unexpected portable MCP configuration")
    servers = mcp.get("mcpServers")
    if not isinstance(servers, dict) or set(servers) != {"keypool"}:
        raise ValueError("Expected only the KeyPool MCP server")
    server = servers["keypool"]
    if not isinstance(server, dict) or set(server) != {"type", "url"}:
        raise ValueError("Unexpected portable MCP server fields")
    if server["type"] != "streamable-http":
        raise ValueError("Unexpected portable MCP transport")
    url = server["url"]
    if not isinstance(url, str):
        raise ValueError("Expected a KeyPool MCP URL")
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.netloc != "keypool.whatsinfor.me"
        or parsed.path != "/mcp"
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Unexpected KeyPool MCP URL")

    if args.chatgpt_base_archive:
        payloads, manifest = cloud_plugin_payloads(args, payloads)
        destination = ROOT / "dist" / "keypool-chatgpt-cloud"
    elif args.chatgpt_app_id:
        # ChatGPT web uses the existing registered app. Declaring either MCP
        # configuration file would make this imported package desktop-only.
        del payloads["mcp.json"]
        manifest["name"] = "keypool-workflows"
        openai = manifest["extensions"]["com.openai"]
        openai.pop("review", None)
        openai.pop("publication", None)
        openai["apps"] = "./.app.json"
        openai["interface"]["displayName"] = "KeyPool workflows"
        openai["interface"]["shortDescription"] = "Search, speech, and data"
        payloads["plugin.json"] = json_bytes(manifest)
        payloads[".app.json"] = json_bytes(
            {"apps": {"keypool": {"id": args.chatgpt_app_id, "required": True}}}
        )
        # Updates overlay existing files. Refresh the compatibility manifest
        # explicitly so an older generated manifest cannot keep an old version.
        payloads[".codex-plugin/plugin.json"] = json_bytes(
            {
                "name": manifest["name"],
                "version": manifest["version"],
                "description": manifest["description"],
                "skills": "./skills/",
                "apps": "./.app.json",
                "author": {"name": openai["interface"]["developerName"]},
                "interface": openai["interface"],
            }
        )
        # The app reference supplies the connection; this variant does not ask
        # the host to register another MCP server through skill dependencies.
        payloads["skills/keypool/agents/openai.yaml"] = (
            'interface:\n'
            '  display_name: "KeyPool workflows"\n'
            '  short_description: "Search, speech, and data"\n'
        ).encode("utf-8")
        destination = ROOT / "dist" / "keypool-chatgpt"
    elif args.target == "public":
        # Portal imports MCP + skills and creates its own app binding. Never
        # upload a personal .app.json or the legacy Agents API auth overlay.
        if manifest.get("apps") is not None or manifest["extensions"]["com.openai"].get("apps") is not None:
            raise ValueError("Public submissions cannot contain app references")
        destination = ROOT / "dist" / "keypool-public"
    else:
        add_agents_api_overlay(payloads, manifest, url)
        destination = DESTINATION

    package_name = manifest["name"]
    package = prepare_output(destination, package_name, payloads)
    for name, content in payloads.items():
        target = package / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    archive_path = destination / f"{package_name}.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(payloads):
            archive_name = name if args.chatgpt_base_archive else f"{package_name}/{name}"
            info = zipfile.ZipInfo(archive_name, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, payloads[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    print(f"Wrote {archive_path.relative_to(ROOT)} ({len(payloads)} files)")


def cloud_plugin_payloads(args, canonical: dict[str, bytes]) -> tuple[dict[str, bytes], dict]:
    """Add canonical skills to a downloaded cloud package without changing its app."""
    require_regular_file(args.chatgpt_base_archive)
    required = {".app.json", ".codex-plugin/plugin.json"}
    skill_files = {name for name in canonical if name.startswith("skills/")}
    allowed = required | skill_files
    with zipfile.ZipFile(args.chatgpt_base_archive) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        if (len(names) != len(set(names)) or not required <= set(names)
                or not set(names) <= allowed or sum(entry.file_size for entry in entries) > 10 * 1024 * 1024
                or any(stat.S_IFMT(entry.external_attr >> 16) not in (0, stat.S_IFREG) for entry in entries)):
            raise ValueError("Unexpected cloud plugin archive inventory or file type")
        payloads = {entry.filename: archive.read(entry) for entry in entries}

    manifest = json.loads(payloads[".codex-plugin/plugin.json"])
    app = json.loads(payloads[".app.json"])
    if (not isinstance(manifest, dict) or manifest.get("name") != args.chatgpt_package_name
            or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", args.chatgpt_package_name)):
        raise ValueError("Cloud plugin package identity mismatch")
    apps = app.get("apps") if isinstance(app, dict) else None
    binding = next(iter(apps.values())) if isinstance(apps, dict) and len(apps) == 1 else None
    if (not isinstance(apps, dict) or len(apps) != 1
            or not isinstance(binding, dict) or binding.get("id") != args.chatgpt_app_id
            or manifest.get("apps") != "./.app.json" or manifest.get("mcpServers") is not None
            or manifest.get("skills") not in (None, "./skills", "./skills/")):
        raise ValueError("Cloud plugin app binding or component mismatch")
    previous = manifest.get("version", "")
    if not all(isinstance(version, str) and re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version)
               for version in (previous, args.chatgpt_version)):
        raise ValueError("Cloud plugin versions must be strict semantic versions")
    if tuple(map(int, args.chatgpt_version.split("."))) <= tuple(map(int, previous.split("."))):
        raise ValueError("Cloud plugin version must increase")
    interface = manifest.get("interface")
    if not isinstance(interface, dict) or not isinstance(interface.get("displayName"), str):
        raise ValueError("Missing cloud plugin presentation metadata")
    manifest["version"] = args.chatgpt_version
    manifest["skills"] = "./skills/"
    payloads[".codex-plugin/plugin.json"] = json_bytes(manifest)
    for name in skill_files:
        payloads[name] = canonical[name]
    # Existing app registration owns tools/OAuth; avoid an additional MCP dependency.
    payloads["skills/keypool/agents/openai.yaml"] = (
        f'interface:\n  display_name: {json.dumps(interface["displayName"])}\n'
        '  short_description: "Search, speech, and data"\n'
    ).encode("utf-8")
    return payloads, manifest


def add_agents_api_overlay(payloads: dict[str, bytes], manifest: dict, url: str) -> None:
    payloads[".codex-plugin/plugin.json"] = json_bytes(
        {
            "name": manifest["name"],
            "version": manifest["version"],
            "description": manifest["description"],
            "skills": "./skills/",
            "mcpServers": "./.mcp.json",
        }
    )
    payloads[".mcp.json"] = json_bytes(
        {
            "mcpServers": {
                "keypool": {
                    "type": "http",
                    "url": url,
                    "bearer_token_env_var": "KEYPOOL_MCP_ACCESS_TOKEN",
                }
            }
        }
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"Plugin export failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
