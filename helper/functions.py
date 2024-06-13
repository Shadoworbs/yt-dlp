import os
import math


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


# search the current directory for a file and convert it's size to readable format
def search(id:str=None, raw_reso:str=None, ext=None, mode='audio') -> str:
    if mode == 'audio':
        with os.scandir(os.getcwd()) as files:
            for file in files:
                if (id in file.name 
                    and os.path.isfile(file)
                    and file.name.endswith(ext)):
                    size_ = os.path.getsize(file)
    elif mode == 'video':
        with os.scandir(os.getcwd()) as files:
            for file in files:
                if (id in file.name 
                    and os.path.isfile(file)
                    and file.name.endswith(ext)
                    and raw_reso in file.name
                    ):
                    size_ = os.path.getsize(file)
    else:
        raise ValueError("Invalid mode. Choose 'video' or 'audio'")
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
def getsize(id:str=None, raw_reso:str=None, ext=None, mode='video') -> str:
    if mode.lower() == 'video':
        try:
            size = search(id, raw_reso, ext)
            return size
        except FileNotFoundError as e:
            print(f'\nError in getsize: 1st try statement: \n{e}\n')
            return None
        except Exception as e:
            print(f'An error occured in getsize 1st exception: \n{e}\n')
            return '0B'
    elif mode.lower() == 'audio':
        # try:
        size = search(id=id, ext=ext)
        return size
        # except FileNotFoundError as e:
        #     print(f'\nError in getsize: 2nd try statement: \n{e}\n')
        #     return None
        # except Exception as e:
        #     print(f'\nAn error occured in getsize 2nd except: \n{e}\n')
        #     return '0B'
    else:
        return None


# # renamer function
# def renamer(infos:tuple)-> None:
#     original_title, ext, id, reso, cwd, raw_res, sec_name, mode = infos
#     if mode == 'video':
#         try:
#             os.chdir('videos')
#         except:
#             pass
#         _, file = search(id, raw_res, ext)
#         try:
#             os.rename(file, fr"{original_title}-{id}.{ext}")
#         except FileNotFoundError as e:
#             print(f"Error in renamer: \n{e}")
#         except FileExistsError as e:
#             print(f'An error occured: \n{e}')
#         except Exception as e:
#             print(f'{e}')

#     elif mode == 'audio':
#         try:
#             os.chdir('audio')
#         except: 
#             pass
#         _, file = search(sec_name, ext)
#         try:
#             os.rename(file, fr'{original_title}-{id}.{ext}')
#         except FileNotFoundError as e:
#             print(f"Error in renamer: \n{e}")
#         except FileExistsError as e:
#             print(f'An error occured: \n{e}')
#         except Exception as e:
#             print(f'{e}')

