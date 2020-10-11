from pathlib import Path

import moviepy.editor


def to_mp3(input_file):
    with moviepy.editor.AudioFileClip(input_file) as clip:
        mp3_path = Path(input_file).with_suffix('.mp3').resolve()
        clip.write_audiofile(mp3_path, verbose=False, logger=None)
        Path(input_file).unlink(missing_ok=True)
