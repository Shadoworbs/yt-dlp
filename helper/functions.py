import os
import math

SIZE_NAME = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")


# logger function
def log(inf: dict) -> None:
    with open(".log", "a", encoding="utf-8") as log:
        for key in inf:
            log.write(f"""{key}: {inf[key]}\n""")
        log.write("\n\n")


# seconds converter
def convert_seconds(seconds) -> str:
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    # {days}d
    duration = f"{hours}h {minutes}m {seconds}s"
    return duration


# search the current directory for the downloaded file and convert it's size to a readable format
def getsize(timestamp) -> str:
    with os.scandir(os.getcwd()) as files:
        for file in files:
            if (timestamp in file.name 
                and os.path.isfile(file)):
                size_ = os.path.getsize(file)
            else:
                # if the file is not found
                size_ = 0
            
    # convert the size from bytes to readable format
    if size_ == 0:
        return "0B"
    i = int(math.floor(math.log(size_, 2) / math.log(1024, 2)))
    p = math.pow(1024, i)
    s = round(size_ / p, 2)
    formatted_size = f"{s} {SIZE_NAME[i]}"
    return formatted_size
