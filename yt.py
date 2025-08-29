# This is an open source project created by shadoworbs for downloading youtube video/audio
# Source Code https://github.com/shadoworbs/yt-dlp

# import the necessary modules
from helper.downloaders import YoutubeDownloader

## initiate the download https://youtube.com/shorts/ANSdr07F-XA?si=4RIxliQBkKvMpcdv
if __name__ == "__main__":
    downloader = YoutubeDownloader()
    downloader.start_downloading()