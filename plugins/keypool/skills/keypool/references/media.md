# Speech and subtitles

Speech synthesis is available from Cartesia and Deepgram. Discover voices or TTS models using the provider's discovery tool, then supply the actual identifier. Choose output format based on the user's delivery target. Keep the user's text and pronunciation intent intact. Voice cloning, transcription, and voice conversion are outside this plugin.

For subtitles, search SubDL or OpenSubtitles by title or provider-supported media identifiers and select the matching language, release, season, and episode. Preserve search-result identifiers. SubDL downloads use only the returned KeyPool subtitle path. OpenSubtitles downloads use file IDs and KeyPool's managed upstream accounts; users do not need an OpenSubtitles password or session token.

Download through the corresponding tool, then return the generated KeyPool file link. Check whether the provider returned an archive or a subtitle text file and label it accordingly. A successful search does not establish download availability. Report quota or unavailable-account errors directly.
