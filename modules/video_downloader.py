from __future__ import unicode_literals
from datetime import datetime
import os
from yt_dlp import YoutubeDL
from modules.converter import convert_seconds
from modules.calculate_size import getsize
from modules.logger import log


# function to download the video only
def download_video(url, video_height, fps=25):
    if os.path.exists('videos'):
        try:
            os.chdir('videos')
        except:
            print("Can't change directory to /videos")
            pass
    else:
        try:
            os.mkdir('videos')
            os.chdir('videos')
        except:
            print("Can't create directory /videos")
            pass

    # set up the video download options
    opts = {"trim_file_name": 200,
            "format": f"((bv*[fps>={fps}]/bv*)[height<={video_height}]/(wv*[fps>={fps}]/wv*)) + ba / (b[fps>{fps}]/b)[height<={video_height}]/(w[fps>={fps}]/w)",
            "playlist": True,
            "outtmpl": "%(title)s.%(ext)s",
            "audio_format": "mp3",
            "video_format": "mp4",
            "audio_quality": "32",
            "audio_codec": "aac",
            "audio_bitrate": "32k",
            "audio_channels": "2",
            "audio_samplerate": "11025",
            "merge_output_format": "mp4"}
    with YoutubeDL(opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title: str = info_dict.get('title', str)
        extension = info_dict.get('ext', str)
        # dur: str = info_dict.get('duration_string', str)
        res: str = info_dict.get('resolution', str)
        size: str = info_dict.get('filesize')
        # video_id: str = info_dict.get('id', str)
        video_duration = info_dict.get('duration', str)
        reso = res.split('x')[-1] or video_height

    # prepare a info for logging
    get_size = getsize(video_title)
    log_inf = {"Video Name": f'{video_title}.mp4',
                "Location": os.getcwd(),
                "Duration": convert_seconds(video_duration),
                "Resolution": f'{reso}p',
                "Size": get_size,
                "Link": url,
                "Date": f'{datetime.now().strftime("%A, %B %d %Y | %I:%M %p")}'}
    
    # print a success message after download completes
    print(f"""
Download complete!
Video name: {video_title}.mp4
Video location : {os.getcwd()}
Video duration: {convert_seconds(video_duration)}
Video resolution: {reso}p
Video Size: {get_size}
""")
    
    # log the video information
    log(log_inf)