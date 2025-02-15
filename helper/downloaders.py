from __future__ import unicode_literals
from datetime import datetime
from yt_dlp import YoutubeDL
from helper.functions import getsize, convert_seconds, log
from config import video_merge_output_format as final_extension, video_format_selection_options as formats_
import os

cwd = os.getcwd()
now = datetime.now
audio_folder, video_folder = "audio", "videos"
timestamps = now().strftime('%Y%m%d%H%M%S')

###############################################
###########    Video Downloader   #############
###############################################

# function to download video only
def download_video(url, video_height, fps=30) -> tuple:
    """
    Downloads the video from the given URL, resizes it to the specified height,
    and saves it as a mp4 file with a unique timestamp and extension.
    """
    if os.path.exists(video_folder):
        try:
            os.chdir(video_folder)
        except Exception as e:
            print(f"Can't change directory to {video_folder} \n{e}")
            pass
    else:
        try:
            os.mkdir(video_folder)
            os.chdir(video_folder)
        except Exception as e:
            print(f"Can't create directory {video_folder}\n{e}")
            pass

    # set up the video download options
    opts = {"trim_file_name": 200,
            'outtmpl': '%(title)s_{timestamps}.%(ext)s'.format(timestamps=timestamps),
            "encoding": "utf-8",
            "format": formats_.format(video_height, fps, video_height, fps),
            # "playlist": True,
            "cookiefile": "cookies_from_browser firefox",
            "merge_output_format": final_extension
            } # using a merge output format that will result in a low size video wihout sacrificing quality
    with YoutubeDL(opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title: str = info_dict.get('title', str)
        extension = info_dict.get('ext', str)
        # dur: str = info_dict.get('duration_string', str)
        raw_resolution: str = info_dict.get('resolution', str)
        # size: str = info_dict.get('filesize')
        # video_id: str = info_dict.get('id', str)
        video_duration = info_dict.get('duration', str)
        video_resolution = raw_resolution.split('x')[-1] or video_height

    # assign the return value ofconvert_seconds function to a variable
    readable_duration = convert_seconds(video_duration)
    # assign the return value of getsize function to a variable
    get_size = getsize(timestamps)
  
    # prepare a info (dict) for logging
    log_inf = {"Video Name": f'{video_title}_{timestamps}.{extension}',
                "Location": f"{os.path.join(cwd, video_folder)}",
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
Video name: {video_title}_{timestamps}.{extension}
Video location : {os.path.join(cwd, video_folder)}
Video duration: {readable_duration}
Video resolution: {video_resolution}p
Video Size: {get_size}""")

###############################################
###########    Audio Downloader   #############
###############################################

# function to download the audio only
def download_audio(url):
    """
    Downloads the audio from the given URL and saves it as a m4a file with a unique timestamp."""
    # Create folders for storing downloaded media
    if os.path.exists(audio_folder):
        try:
            os.chdir(audio_folder)
        except:
            print(f"Couldn't change directory to {audio_folder}")
            pass
    else:
        try:
            os.mkdir(audio_folder)
            os.chdir(audio_folder)
        except:
            print(f"Couldn't create directory {audio_folder}")
            pass
    # start the dowload process
    with YoutubeDL({'extract_audio': True, 
                            "format": "bestaudio[ext=m4a]/b", 
                            'outtmpl': '%(title)s_{timestamps}.%(ext)s'.format(timestamps=timestamps),
                            "cookiefile": "cookies_from_browser firefox"}) as audio:
        info_dict = audio.extract_info(url, download=True) # download the audio
        audio_title = info_dict['title'] # extract the title from the url info.json
        extension = info_dict['ext'] # extract the extension from the url info.json
        audio_duration = info_dict.get('duration', str)  # extract the duration fron the url info.json
        # audio_id = info_dict.get('id', str) # get the audio id

        # assign the return value of convert seconds functioni to a varible
        readable_duration = convert_seconds(audio_duration)
        # assign the return value of getsize to a variable
        get_size = getsize(timestamps)

        # set up the audio information dictionary for logging
        audio_infos = {"Title": f'{audio_title}_{timestamps}.{extension}',
                        "Location": f"{os.path.join(cwd, audio_folder)}",
                        "Duration": readable_duration,
                        "Size": get_size,
                        "Timestamp": f'{now().strftime("%A, %B %d %Y | %I:%M %p")}'}
        
        # log the audio information to a log file
        log(audio_infos)

        # print success message after downloading is complete
        print(f"""
Download complete!
Title: {audio_title}_{timestamps}.{extension}
location: {os.path.join(cwd, audio_folder)}
Duration: {readable_duration}
Size: {get_size}
""")