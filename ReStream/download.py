import youtube_dl


class Downloader:
    def download(self, video):
        downloader = youtube_dl.downloader.FileDownloader(video, {})
        downloader.download(downloader, {})
