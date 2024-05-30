# import the necessary modules
import math
import os

def search(title, ext='.mp4'):
        with os.scandir(os.getcwd()) as files:
                for file in files:
                    filename_lenght = len(os.path.basename(file))
                    if (os.path.basename(file) == f"{title}.mp4" or file.name == title[:filename_lenght//2]
                        and os.path.isfile(file)):
                        size_ = os.path.getsize(file)
                        # convert the size from bytes to readable format
                        if size_ == 0:
                            return "0B"
                        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
                        i = int(math.floor(math.log(size_, 1024)))
                        p = math.pow(1024, i)
                        s = round(size_ / p, 2)
                        size_ = "%s %s" % (s, size_name[i])
                        return size_
                    
# function to get stats of downloaded file
def getsize(title, mode='video', ext='.mp4'):
    if mode.lower() == 'video':
        try:
            os.chdir("videos")
            size = search(title)
            return size
        except:
            size = search(title)
            return size
    elif mode.lower() == 'audio':
        try:
            os.chdir("audio")
            size = search(title, ext=ext)
            return size
        except:
            size = search(title, ext=ext)
            return size
