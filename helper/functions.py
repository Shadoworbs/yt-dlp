import os
import math

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
def find_downloaded_video(timestamp: int) -> int:
    """
    Searches the current directory for the downloaded video file and returns it's size in bytes."""
    with os.scandir(os.getcwd()) as files:
        for file in files:
            if (timestamp in file.name 
                and os.path.isfile(file)):
                size_ = os.path.getsize(file)
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
