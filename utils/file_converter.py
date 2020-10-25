from pathlib import Path

# import moviepy.editor
# to prevent error in 'pyinstaller': module 'moviepy.audio.fx.all' has no attribute 'audio_fadein'
from moviepy.audio.io.AudioFileClip import AudioFileClip
# from moviepy.audio.fx.audio_fadein import audio_fadein
# from moviepy.audio.AudioClip import write_audiofile


def to_mp3(input_file):
    # with moviepy.editor.AudioFileClip(input_file) as clip:
    with AudioFileClip(input_file) as clip:
        mp3_path = Path(input_file).with_suffix('.mp3').resolve()
        clip.write_audiofile(mp3_path, verbose=False, logger=None)
        Path(input_file).unlink(missing_ok=True)


# examples:
# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.video.fx.resize import resize
# VideoFileClip.resize = resize
# clip = VideoFileClip(path).resize((255,255))

# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.video.VideoClip import ImageClip
# from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
