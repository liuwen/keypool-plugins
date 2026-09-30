# Speech and subtitles

## Speech

- `cartesia_list_voices` returns voice IDs. Supply a returned `voice_id` and an explicitly known Cartesia `model_id` to `cartesia_synthesize_speech`. Voice discovery does not discover models; do not invent a model ID. This tool requests WAV, PCM signed 16-bit little endian, 16 kHz. It has no output-format parameter.
- `deepgram_list_models` returns TTS models. Supply an actual Aura TTS model identifier as `model` to `deepgram_synthesize_speech`. This tool uses the provider's default MP3 delivery and has no output-format parameter.
- Both synthesis tools accept at most 4,000 characters and consume provider quota. Preserve the requested text, language, and pronunciation intent. The returned artifact metadata determines the actual delivered media type. If the user needs another format, explain the tool's format before generating.

Voice cloning, transcription, and voice conversion are outside this plugin.

## Subtitles

| Provider | Search | Download identifier |
| --- | --- | --- |
| SubDL | Supply `film_name`, `file_name`, `imdb_id` in `tt1234567` form, or numeric `tmdb_id`. Optional movie/TV type, season, episode and comma-separated language codes narrow the match. | Copy the returned `/v1/subdl/subtitle/...` path into `download_path`. Do not supply an absolute URL, movie ID, or title to the download tool. |
| OpenSubtitles | `query` is a title/text search. Optional languages, season, episode, year and page narrow it. This tool has no IMDb ID or file-hash search parameter. | Take the positive `file_id` from a matched result's `attributes.files[]`. Do not use the search record's `id`, feature ID, IMDb ID, or filename. |

Select the match by title, language, release and, for TV, season and episode before downloading. When the match is ambiguous, clarify or present the relevant candidates instead of guessing. Language filters use comma-separated two- or three-letter provider codes, not language names.

`opensubtitle_download_subtitle` uses KeyPool's managed upstream accounts. The caller does not provide an OpenSubtitles password or session token. Search success does not prove that download quota or an eligible managed account is available.

Download through the corresponding tool and return the private artifact link. Label the actual `mime_type`: a SubDL result may be a ZIP archive or a subtitle text file. Do not promise SRT from a filename alone. Report quota, unavailable-account, or download errors directly.
