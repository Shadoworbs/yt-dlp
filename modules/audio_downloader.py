from __future__ import unicode_literals
from datetime import datetime
import os
from yt_dlp import YoutubeDL
from modules.converter import convert_seconds
from modules.calculate_size import getsize
from modules.logger import log


# function to download the audio only
def download_audio(url):
    
    if os.path.exists('audio'):
        try:
            os.chdir('audio')
        except:
            print("Can't change directory to /videos")
            pass
    else:
        try:
            os.mkdir('audio')
            os.chdir('audio')
        except:
            print("Can't create directory /audio")
            pass
    with YoutubeDL({'extract_audio': True, 
                            "format": "bestaudio[ext=m4a]/best", 
                            'outtmpl': '%(title)s.%(ext)s'}) as audio:
        info_dict = audio.extract_info(url, download = True)
        audio_title = info_dict['title']
        extension = info_dict['ext']
        audio_duration = info_dict.get('duration', str)

        # set up the audio information dictionary for logging
        get_size = getsize(audio_title, mode='audio', ext=f".{extension}")
        audio_infos = {"Title": f'{audio_title}.{extension}',
                        "Location": os.getcwd(),
                        "Duration": convert_seconds(audio_duration),
                        "Size": get_size,
                        "Date": f'{datetime.now().strftime("%A, %B %d %Y | %I:%M %p")}'}

        # print success message after downloading the audio
        print(f"""
Download complete!
Title: {audio_title}.{extension}
location: {os.getcwd()}
Duration: {convert_seconds(audio_duration)}
Size: {get_size}
""")
        # log the audio information to a log file
        log(audio_infos)