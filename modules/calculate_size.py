# import the necessary modules
import math
import os


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
            if (title in file.path
                and file.path.endswith(ext)
                and file.is_file()
                ):
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