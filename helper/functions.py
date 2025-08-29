import os
import math
from time import sleep
from typing import Optional
from config import video_merge_output_format, audio_extension

class VideoProcessor:
    """Class to handle video processing operations including:
    logging, 
    duration conversion, 
    and file size calculations."""
    
    SIZE_NAME = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    
    @staticmethod
    def log_post_download_info(inf: dict) -> None:
        """
        Logs the video information to a file named .log in the current directory.
        
        Args:
            inf (dict): Dictionary containing video information to log
        """
        with open(".log", "a", encoding="utf-8") as log:
            for key in inf:
                log.write(f"{key}: {inf[key]}\n")
            log.write("\n\n")
    
    @staticmethod
    def convert_video_duration_from_seconds(seconds: int) -> str:
        """
        Convert seconds to a human-readable duration format.
        
        Args:
            seconds (int): The duration in seconds to convert

        Returns:
            str: Duration in format "XhYmZs" where X=hours, Y=minutes, Z=seconds
            
        Example:
            >>> VideoProcessor.convert_video_duration_from_seconds(3665)
            '1h 1m 5s'
        """
        seconds = int(seconds)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return f"{hours}h {minutes}m {seconds}s"
    
    @staticmethod
    def find_downloaded_video(timestamp: int, file_path: str) -> Optional[int]:

        """
        Find a downloaded video file by timestamp and return its size.
        
        Args:
            timestamp (int): The timestamp to look for in the video filename
            video_path (str, optional): Directory path to search. Defaults to "videos"
            
        Returns:
            Optional[int]: Size of found video in bytes, or None if not found
        """

        combined_formats = [video_merge_output_format, audio_extension]

        print("Cleaning up the junk...\n")
        sleep(1)
        try:
            os.chdir(os.path.join(os.getcwd(), file_path))
        except FileNotFoundError:
            pass
            
        with os.scandir(os.getcwd()) as files:
            for file in files:
                if (str(timestamp) in file.name 
                    and file.is_file()
                    and file.name.endswith(tuple(combined_formats))):
                    return file.stat().st_size
        return None
    
    @classmethod
    def convert_bytes_to_readable_format(cls, timestamp: int, file_path="videos") -> str:
        """
        Convert file size to human-readable format.
        
        Args:
            timestamp (int): Timestamp identifier for the video file
            
        Returns:
            str: Human-readable file size (e.g., "1.5 MB", "800 KB")
        """
        size_of_video = cls.find_downloaded_video(timestamp=timestamp, file_path=file_path)
        
        if size_of_video is None:
            return "0B"
            
        i = int(math.floor(math.log(size_of_video, 2) / math.log(1024, 2)))
        p = math.pow(1024, i)
        s = round(size_of_video / p, 2)
        return f"{s} {cls.SIZE_NAME[i]}"
