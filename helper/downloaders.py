from __future__ import unicode_literals
from datetime import datetime
import sys
import yt_dlp
from yt_dlp import YoutubeDL
from helper.functions import (convert_bytes_to_readable_format as getsize, 
                              convert_video_duration_from_seconds as convert_seconds,
                              log_post_download_info as log)
from config import (video_merge_output_format as final_extension, 
                    video_format_selection_options as formats_)
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: [%(asctime)s] %(message)s',
                    datefmt='%H:%M %p')
cwd = os.getcwd()
now = datetime.now
audio_folder, video_folder = "audio", "videos"
timestamps = now().strftime('%Y%m%d%H%M%S')

def pre_download_options() -> tuple:
    """
    - Function to get the user's input before downloading the video.
        - accepts the user's input (url)
            - If the user enters a valid youtube video link, asks if they want to download the audio only.
            - If the user enters an invalid link, it prompts the user to enter a valid link.
            - and if the user enters nothing, the program exits.
        - Returns the url and the available formats.
        - Throws an exception if the user enters an invalid link.
    """
     # create a variable to store the link from the user
    url = input('\nEnter a youtube video link or press enter to exit: \n')
    if ('https://' in url 
        and 'youtu' in url):

        audio_only = input('\nDo you want to download the audio only? (y/n) \n')

        # check if user wants to download audio only
        if (audio_only.lower() == 'y'):
            download_audio(url)
            sys.exit() # exit the program if user wants to download audio only
    
        # download the video
        elif (audio_only.lower() != 'y'):

            # show available formats
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get available formats
                formats = ydl.extract_info(url, download=False)['formats']

                # Filter valid resolutions only
                filtered_formats = []
                for format in formats:
                    resolution = f"{format.get('height')}"
                    fps = f"{format.get('fps')}"
                    if (resolution not in filtered_formats
                        and resolution is not None
                        and resolution != 'None'):

                        filtered_formats.append(resolution) # getting rid of all duplicates and None(s)
                # show available resolutions (formats)
                if filtered_formats:
                    print("\n[+]Available Resolutions:")
                    print(" #  Resolutions")
                    print("="*15)
                    for number, height in enumerate(filtered_formats):
                        resolution = height
                        print(f"{(number+1):2}. {str(resolution):<12}")
                else:
                    print("No available formats found.")
    elif 'youtu' not in url and len(url) >= 1:
            print("\nInvalid youtube link, try again.\n")
    else:
        sys.exit(0)
    return url, filtered_formats


def start_downloading() -> None:
    """
    Main function to initiate the download.
    - Calls the pre_download_options function to get the user's input.
    - Calls the download_video function to initiate the video download.
     """
    print(f"\n{"=" * 15} Welcome to yt-dlp! {"=" * 15}\n")
    url, filtered_formats = pre_download_options()
    
    # select video quality (height)
    while True:
        try:
            choice = int(input("Enter the number of the resolution you want to download (or 0 to cancel): "))
            if 1 <= choice <= len(filtered_formats): # Check if choice is within range and not 0
                break
            elif int(choice) == 0:
                sys.exit()
            else:
                # if choice is not within range or is 0
                print(f"Invalid choice. Please enter a number from 1 to {len(filtered_formats)}\n")
        except ValueError:
            # if user inputs a value that is not a number
            print("Invalid input. Please enter a number.\n")
    # set the height to selected format's height.
    video_height = filtered_formats[choice - 1]
    download_video(url, video_height)


###############################################
###########    Video Downloader   #############
###############################################

# function to download video only
def download_video(url, video_height, fps=30) -> tuple:
    """
    Downloads the video from the given URL, resizes it to the specified height,
    and saves it as a video file with a unique timestamp and extension.
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
            "playlist": True,
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
    logging.info(f"""
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
def download_audio(url) -> None:
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
        logging.info(f"""
Download complete!
Title: {audio_title}_{timestamps}.{extension}
location: {os.path.join(cwd, audio_folder)}
Duration: {readable_duration}
Size: {get_size}
""")