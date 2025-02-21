import os
import math
from time import sleep

SIZE_NAME = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

# logger function
def log_post_download_info(inf: dict) -> None:
    """
    Logs the video information to a file named .log in the current directory.
    """
    with open(".log", "a", encoding="utf-8") as log:
        for key in inf:
            log.write(f"""{key}: {inf[key]}\n""")
        log.write("\n\n")

# seconds converter
def convert_video_duration_from_seconds(seconds) -> str:
    """
    Converts seconds to a human-readable duration format.
    """
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    # {days}d
    duration = f"{hours}h {minutes}m {seconds}s"
    return duration

# search the current directory for the downloaded file and convert it's size to a readable format
def find_downloaded_video(timestamp: int, video_path="videos") -> int:
    '''Searches for a downloaded video file based on a timestamp and returns its size in bytes.

    This function looks for a video file in the specified directory (or current directory) that contains
    the given timestamp in its filename. If found, returns the file size in bytes.

    Args:
        timestamp (int): The timestamp to search for in the video filename
        video_path (str, optional): The directory path where videos are stored. Defaults to "videos".

    Returns:
        int: The size of the found video file in bytes. Returns 0 if no matching file is found.

    Raises:
        OSError: If there are issues accessing the directory or file
        TypeError: If timestamp is not an integer

    Example:
        >>> find_downloaded_video(1234567890)
        1048576  # Returns size in bytes for video file containing timestamp 1234567890
        >>> find_downloaded_video(9999999999)
        0  # Returns 0 if no matching file is found'''
    print("Cleaning up the junk...\n")
    sleep(1)
    try:
        os.chdir(os.path.join(os.getcwd(), video_path))
    except:
        pass
    with os.scandir(os.getcwd()) as files:
        for file in files:
            if (timestamp in file.name 
                and file.is_file()
                and file.name.endswith((".mkv"))):
                size_ = file.stat().st_size
                break
            else:
                # if the file is not found
                size_ = 0
    return size_

def convert_bytes_to_readable_format(timestamp) -> str:
    """
    Converts the size of the downloaded video to a human-readable format.
    """
    size_of_video: int = find_downloaded_video(timestamp=timestamp)       
    # convert the size from bytes to readable format
    if size_of_video == 0:
        return "0B"
    i = int(math.floor(math.log(size_of_video, 2) / math.log(1024, 2)))
    p = math.pow(1024, i)
    s = round(size_of_video / p, 2)
    formatted_size = f"{s} {SIZE_NAME[i]}"
    return formatted_size
