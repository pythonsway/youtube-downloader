import io
import re
import time
from pathlib import Path

from pytube import YouTube

from utils.file_converter import to_mp3


class YouTubeDownloader:
    def __init__(self):
        self.yt = None
        self.download_option = None
        self.title = None
        self.thumbnail_url = None
        self.length = None
        self.author = None
        self.streams_list = []
        self.downloaded_clip = None

    def list_streams(self):
        # [<Stream: itag="22" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.64001F" acodec="mp4a.40.2">,
        #  <Stream: itag="14" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2">]
        if self.download_option == 1:
            for stream in self.yt.streams.filter(progressive=True):
                if stream.video_codec:
                    self.streams_list.append((stream.itag,
                                              stream.mime_type.split('/')[1],
                                              f'{stream.resolution}({stream.fps}fps)',
                                              float(f'{stream.filesize / 1024**2:.2f}')))
        elif self.download_option == 2:
            for stream in self.yt.streams.filter(only_audio=True):
                self.streams_list.append((stream.itag,
                                          stream.mime_type.split('/')[1],
                                          stream.abr,
                                          float(f'{stream.filesize / 1024**2:.2f}')))

    def check(self, url, download_option):
        self.yt = YouTube(url)
        self.download_option = download_option
        self.title = self.yt.title
        # https://i.ytimg.com/vi/_________/default.jpg
        thumbnail_pattern = re.compile(r'[\w\d]+.jpg$')
        self.thumbnail_url = thumbnail_pattern.sub('default.jpg', self.yt.thumbnail_url)
        self.length = time.strftime("%H:%M:%S", time.gmtime(self.yt.length))
        self.author = self.yt.author
        self.streams_list.clear()
        self.list_streams()

    def download(self, itag, path, name):
        self.downloaded_clip = self.yt.streams.get_by_itag(itag).download(output_path=path, filename=name,
                                                                          skip_existing=False)

    def file_complete(self):
        if self.download_option == 2:
            return False
        else:
            return True

    def file_converter(self, downloaded_clip):
        # p = Path(path)
        # f = p / f'{name}.*'
        to_mp3(downloaded_clip)

    def register_on_progress_callback(self, func):
        self.yt.register_on_progress_callback(func)

    def register_on_complete_callback(self, func):
        self.yt.register_on_complete_callback(func)
