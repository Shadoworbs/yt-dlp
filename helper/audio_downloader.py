from __future__ import unicode_literals
from datetime import datetime
import os
from yt_dlp import YoutubeDL
from helper.converter import convert_seconds
from helper.calculate_size import getsize
from helper.logger import log


# function to download the audio only
def download_audio(url):
    # Create folders for storing downloaded media
    if os.path.exists('audio'):
        try:
            os.chdir('audio')
        except:
            print("Couldn't change directory to 'videos'")
            pass
    else:
        try:
            os.mkdir('audio')
            os.chdir('audio')
        except:
            print("Couldn't create directory 'audio'")
            pass
    # start the dowload process
    with YoutubeDL({'extract_audio': True, 
                            "format": "bestaudio[ext=m4a]/best", 
                            'outtmpl': 'audio-%(id)s.%(ext)s'}) as audio:
        info_dict = audio.extract_info(url, download=True) # download the audio
        audio_title = info_dict['title'] # extract the title from the url info.json
        extension = info_dict['ext'] # extract the extension from the url info.json
        audio_duration = info_dict.get('duration', str)  # extract the duration fron the url info.json
        audio_id = info_dict.get('id', str) # get the audio id

        secondary_title = f'audio-{audio_id}'
        # set up the audio information dictionary for logging
        get_size = getsize(secondary_title, mode='audio', ext=extension) # assign the return value of getsize to a variable
        audio_infos = {"Title": f'{audio_title}.{extension}',
                        "Location": os.getcwd(),
                        "Duration": convert_seconds(audio_duration),
                        "Size": get_size,
                        "Timestamp": f'{datetime.now().strftime("%A, %B %d %Y | %I:%M %p")}'}
        

        # rename the downloaded video from the the id assigned name to the original name
        try:
            os.rename(f'{secondary_title}.{extension}', f'{audio_title}-{audio_duration}.{extension}')
        except Exception as e:
            print(f"Couldn't rename audio file: \n{e}")
            os.remove(f'{secondary_title}.{extension}')
            print('Audio removed from directory.')
            pass

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