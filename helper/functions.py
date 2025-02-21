import os
import math
from time import sleep
from typing import Optional

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
def convert_video_duration_from_seconds(seconds: int) -> str:
    """
    Args:
        seconds (int): The duration in seconds to convert

    Returns:
        str: A formatted string representing the duration in the format "XhYmZs" 
            where X=hours, Y=minutes, Z=seconds
        
    Example:
        >>> convert_video_duration_from_seconds(3665)
        '1h 1m 5s'"""
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    # {days}d
    duration = f"{hours}h {minutes}m {seconds}s"
    return duration

# search the current directory for the downloaded file and convert it's size to a readable format
def find_downloaded_video(timestamp: int, video_path="videos") -> Optional[int]:
    """
    Looks for a downloaded video file with a specific timestamp in its name and returns its size.
    This function searches through files in a specified directory for a video file that contains
    the given timestamp in its name and has a .mkv extension. If found, returns the file size
    in bytes; if not found, returns None.
    Args:
        timestamp (int): The timestamp to look for in the video filename
        video_path (str, optional): The directory path where to search for videos. Defaults to "videos".
    Returns:
        Optional[int]: Size of the found video file in bytes, or None if no matching file is found
    Notes:
        - Function changes the current working directory to the specified video_path
        - Only searches for .mkv files
        - Returns the size of the first matching file found
        - Ignores any FileNotFoundError when changing directory
    Example:
        >>> find_downloaded_video(1234567890)
        1048576  # Returns file size in bytes if found
        >>> find_downloaded_video(9999999999)
        None  # Returns None if no matching file is found
    """

    print("Cleaning up the junk...\n")
    sleep(1)
    try:
        os.chdir(os.path.join(os.getcwd(), video_path))
    except FileNotFoundError:
        pass
    with os.scandir(os.getcwd()) as files:
        for file in files:
            if (str(timestamp) in file.name 
                and file.is_file()
                and file.name.endswith((".mkv"))):
                size_ = file.stat().st_size
                break
            else:
                # if the file is not found
                size_ = None
    return size_

def convert_bytes_to_readable_format(timestamp) -> str:
    """
    Convert file size in bytes to a human-readable format.
    This function takes a timestamp, finds the corresponding video file size in bytes,
    and converts it to a human-readable format (e.g., B, KB, MB, GB, TB).
    Args:
        timestamp (str): The timestamp identifier used to locate the video file
    Returns:
        str: A string containing the file size in a human-readable format with appropriate unit
            Examples: "1.5 MB", "800 KB", "2.1 GB"
            Returns "0B" if no video is found for the given timestamp
    Note:
        The function relies on find_downloaded_video() to get the file size in bytes
        Uses binary (base-2) conversion: 1024 bytes = 1 KB
    """

    size_of_video: Optional[int] = find_downloaded_video(timestamp=timestamp)       
    # convert the size from bytes to readable format
    if size_of_video is None:
        return "0B"
    i = int(math.floor(math.log(size_of_video, 2) / math.log(1024, 2)))
    p = math.pow(1024, i)
    s = round(size_of_video / p, 2)
    formatted_size = f"{s} {SIZE_NAME[i]}"
    return formatted_size
