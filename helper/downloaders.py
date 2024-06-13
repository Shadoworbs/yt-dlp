from __future__ import unicode_literals
from datetime import datetime
from yt_dlp import YoutubeDL
from helper.functions import getsize, convert_seconds, log
import os
cwd = os.getcwd()
now = datetime.now



###############################################
###########    Video Downloader   #############
###############################################

# function to download the video only
def download_video(url, video_height, fps=30) -> tuple:
    if os.path.exists('videos'):
        try:
            os.chdir('videos')
        except Exception as e:
            print(f"Can't change directory to /videos \n{e}")
            pass
    else:
        try:
            os.mkdir('videos')
            os.chdir('videos')
        except Exception as e:
            print(f"Can't create directory /videos\n{e}")
            pass


    # set up the video download options
    opts = {"trim_file_name": 200,
            'outtmpl': '%(title)s_%(id)s_%(resolution)s.%(ext)s',
            "encoding": "utf-8",
            "format": f"((bv*[ext=mp4])[height<={video_height}]/(wv*[ext=mp4]/wv*)) + (ba[ext=mp3]/ba) / (b[fps<={fps}]/b)[height<={video_height}]/(w[fps<={fps}]/w)",
            "playlist": True,
            # "outtmpl": "%(title)s.%(ext)s",
            # "merge_output_format": "mp4"
            } # using a merge output format that will result in a low size video
    with YoutubeDL(opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title: str = info_dict.get('title', str)
        extension = info_dict.get('ext', str)
        # dur: str = info_dict.get('duration_string', str)
        raw_resolution: str = info_dict.get('resolution', str)
        # size: str = info_dict.get('filesize')
        video_id: str = info_dict.get('id', str)
        video_duration = info_dict.get('duration', str)
        video_resolution = raw_resolution.split('x')[-1] or video_height


    # assign the return value convert_seconds to a variable
    readable_duration = convert_seconds(video_duration)
    # assign the return value of getsize function to a variable
    get_size = getsize(video_id, raw_resolution, ext=extension, mode='video')
    # rename the video to it's original name
    # renamer(video_title, extension, video_id, video_resolution, cwd, raw_res=raw_resolution, sec_name=secondary_name)

    
    # prepare a info (dict) for logging
    log_inf = {"Video Name": f'{video_title}_{video_id}_{raw_resolution}.{extension}',
                "Location": cwd,
                "Duration": readable_duration,
                "Resolution": f'{video_resolution}p',
                "Size": get_size,
                "Link": url,
                "Timestamp": f'{now().strftime("%A, %B %d %Y | %I:%M %p")}'}
    
    # log the video information
    log(log_inf)


    # print a success message after download completes
    print(f"""
Download complete!
Video name: {video_title}_{video_id}_{raw_resolution}.{extension}
Video location : {cwd}
Video duration: {readable_duration}
Video resolution: {video_resolution}p
Video Size: {get_size}
""")
    



###############################################
###########    Audio Downloader   #############
###############################################

# function to download the audio only
def download_audio(url):
    # Create folders for storing downloaded media
    if os.path.exists('audio'):
        try:
            os.chdir('audio')
        except:
            print("Couldn't change directory to 'audio'")
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
                            "format": "bestaudio[ext=m4a]/b", 
                            'outtmpl': '%(title)s_%(id)s.%(ext)s'}) as audio:
        info_dict = audio.extract_info(url, download=True) # download the audio
        audio_title = info_dict['title'] # extract the title from the url info.json
        extension = info_dict['ext'] # extract the extension from the url info.json
        audio_duration = info_dict.get('duration', str)  # extract the duration fron the url info.json
        audio_id = info_dict.get('id', str) # get the audio id


        # assign the return value of convert seconds functioni to a varible
        readable_duration = convert_seconds(audio_duration)
        # assign the return value of getsize to a variable
        get_size = getsize(id=audio_id, ext=extension, mode='audio')


        # set up the audio information dictionary for logging
        audio_infos = {"Title": f'{audio_title}_{audio_id}.{extension}',
                        "Location": cwd,
                        "Duration": readable_duration,
                        "Size": get_size,
                        "Timestamp": f'{now().strftime("%A, %B %d %Y | %I:%M %p")}'}
        

        # log the audio information to a log file
        log(audio_infos)


        # print success message after downloading is complete
        print(f"""
Download complete!
Title: {audio_title}_{audio_id}.{extension}
location: {cwd}
Duration: {readable_duration}
Size: {get_size}
""")