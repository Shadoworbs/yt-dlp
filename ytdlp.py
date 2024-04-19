# import the necessary modules
from __future__ import unicode_literals
import os
import sys
from yt_dlp import YoutubeDL
from datetime import datetime
from time import sleep
import math
import glob

import yt_dlp


     


# creating a function to create a .log file and write some infos in it
def log(inf: dict) -> None:
    with open(".log", "a", encoding="utf-8") as log:
        for key in inf:
            log.write(f"""{key}: {inf[key]}\n""")
        log.write("\n\n")

# function to change seconds to hours, minutes and seconds
def convert_seconds(seconds) -> str:
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    # {days}d
    duration = f"{hours}h {minutes}m {seconds}s"
    return duration

# function to get stats of downloaded file
def getsize(title, mode='video', ext='.mp4') -> str:
    if mode.lower() == 'video':
        try:
            os.chdir('videos')
        except:
            pass
    elif mode.lower() == "audio":
        try:
            os.chdir('audio')
        except:
            pass
    with os.scandir(os.getcwd()) as files:
        for file in files:
            if title in file.path and ext in file.path and file.is_file():
                file_path: str = file.path
                file_: str = file.name
                size_: int = os.stat(file).st_size
                # convert the size from bytes to readable format
                if size_ == 0:
                    return "0B"
                size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
                i = int(math.floor(math.log(size_, 1024)))
                p = math.pow(1024, i)
                s = round(size_ / p, 2)
                size_ = "%s %s" % (s, size_name[i])
                return size_
            
# function to convert size from bytes to readable format
# def convert_size(size_):
    # if size_ == 0:
    #     return "0B"
    # size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    # i = int(math.floor(math.log(size_, 1024)))
    # p = math.pow(1024, i)
    # s = round(size_ / p, 2)
    # size_ = "%s %s" % (s, size_name[i])
    # return size_

# set up the video download options
# opts = {"trim_file_name": 200,
#         "format": f"((bv*[fps>={fps}]/bv*)[height<={video_height}]/(wv*[fps>={fps}]/wv*)) + ba / (b[fps>{fps}]/b)[height<={video_height}]/(w[fps>={fps}]/w)",
#         "playlist": True,
#         "outtmpl": "%(title)s.%(ext)s",
#         "audio_format": "mp3",
#         "video_format": "mp4",
#         "audio_quality": "128",
#         "audio_codec": "aac",
#         "audio_bitrate": "128k",
#         "audio_channels": "2",
#         "audio_samplerate": "44100",
#         "merge_output_format": "mp4"}

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
        # log the audio information
        log(audio_infos)

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


if __name__ == "__main__":
    # create a variable to store the link from the user
    url = input('\nEnter a youtube video link or press enter to exit: \n')

    audio_only = input('\nDo you want to download the audio only? (y/n) ')
    # check if user wants to download audio only
    if "https://" in url and 'youtu' in url and audio_only.lower() == 'y':
        download_audio(url)
    
    # download the video
    elif "https://" in url and 'youtu' in url and audio_only != 'y':

        # show available formats
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get available formats
            formats = ydl.extract_info(url, download=False)['formats']

            # Filter valid formats with resolution
            unique_resolutions = set()
            filtered_formats = []
            for format in formats:
                resolution = f"{format.get('height', '')}"
                fps = f"{format.get('fps', '')}"
                if resolution and resolution not in unique_resolutions:
                    unique_resolutions.add(resolution)
                    filtered_formats.append(format)
            # Print valid resolutions only
            if filtered_formats:
                print("\nAvailable Resolutions and Framerates:")
                print("  # Resolution    Framerate")
                print("-"*35)
                for i, format in enumerate(filtered_formats):
                    resolution = format['height']  # Use format_id for brevity
                    fps = format['fps']
                    print(f"{(i+1):2}. {str(resolution):<12}  {str(fps):<11}")
                # sys.exit()
            else:
                print("No available formats found.")
        # select video quality and fps or press enter to use the default
        # User selection
        while True:
            try:
                choice = int(input("Enter the number of the format you want to download (or 0 to cancel): "))
                if 0 <= choice <= len(formats):
                    break
                else:
                    print("Invalid choice. Please enter a number between 0 and", len(formats))
            except ValueError:
                print("Invalid input. Please enter a number.")
        # set the height to selected format's height.
        video_height = filtered_formats[choice - 1]["height"]
        download_video(url, video_height)
        # fps = input('\nEnter framerate. Default is 25: ') or '25'
        
    else:
        print("\nInvalid youtube link, try again.")






# TODO:






