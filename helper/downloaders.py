from __future__ import unicode_literals
from datetime import datetime
import sys
import yt_dlp
from yt_dlp import YoutubeDL
from helper.functions import VideoProcessor
from config import (video_merge_output_format as final_extension, 
                   video_format_selection_options as formats_,
                   audio_extension)
import os
import logging

class YoutubeDownloader:
    """Class to handle YouTube video and audio downloads."""
    
    def __init__(self):
        """Initialize the downloader with necessary configurations."""
        self.video_processor = VideoProcessor()
        self.cwd = os.getcwd()
        self.now = datetime.now
        self.audio_folder = "audio"
        self.video_folder = "videos"
        self.timestamps = self.now().strftime('%Y%m%d%H%M%S')
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='\n%(levelname)s: [%(asctime)s] %(message)s',
            datefmt='%H:%M %p'
        )

    def pre_download_options(self) -> tuple:
        """Get user input and return URL and available formats."""
        url = input('\nEnter a youtube video link or press enter to exit: \n')
        
        if 'https://' in url and 'youtu' in url:
            audio_only = input('\nDo you want to download the audio only? (y/n) \n')

            if audio_only.lower() == 'y':
                self.download_audio(url)
                sys.exit()
            
            return self._get_video_formats(url)
            
        elif len(url) >= 1:
            print("\nInvalid youtube link, try again.\n")
        
        sys.exit(0)

    def _get_video_formats(self, url: str) -> tuple:
        """Extract available video formats from URL."""
        with yt_dlp.YoutubeDL({}) as ydl:
            formats = ydl.extract_info(url, download=False)['formats']
            title = ydl.extract_info(url, download=False)['title']
            filtered_formats = self._filter_formats(formats)
            self._display_formats(filtered_formats, title)
            return url, filtered_formats

    def _filter_formats(self, formats: list) -> list:
        """Filter valid video resolutions."""
        filtered_formats = []
        for fmt in formats:
            resolution = f"{fmt.get('height')}"
            if (resolution not in filtered_formats 
                and resolution is not None 
                and resolution != 'None'):
                filtered_formats.append(resolution)
        return filtered_formats

    def _display_formats(self, formats: list, title: str) -> None:
        """Display available video formats."""
        if formats:
            print(f"\n[+] Title: '{title}'")
            print("[+] Resolutions")
            print("="*15)
            for number, height in enumerate(formats, 1):
                print(f"{number:2}. {height:<12}")
        else:
            print("No available formats found.")

    def start_downloading(self) -> None:
        """Main method to initiate the download process."""
        print(f"\n{'=' * 15} Welcome to yt-dlp! {'=' * 15}\n")
        url, filtered_formats = self.pre_download_options()
        
        video_height = self._get_user_choice(filtered_formats)
        self.download_video(url, video_height)

    def _get_user_choice(self, formats: list) -> str:
        """Get user's format choice."""
        while True:
            try:
                choice = int(input("Enter the number of the resolution you want to download (or 0 to cancel): "))
                if 1 <= choice <= len(formats):
                    return formats[choice - 1]
                elif choice == 0:
                    sys.exit()
                print(f"Invalid choice. Please enter a number from 1 to {len(formats)}\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")

    def download_video(self, url: str, video_height: str, fps: int = 30) -> None:
        """Download video with specified parameters."""
        self._prepare_directory(self.video_folder)
        
        opts = {
            "trim_file_name": 200,
            'outtmpl': f'%(title)s_{self.timestamps}.%(ext)s',
            "encoding": "utf-8",
            "format": formats_.format(video_height, fps, video_height, fps),
            "playlist": True,
            "cookiefile": "cookies_from_browser firefox",
            "merge_output_format": final_extension
        }
        
        info = self._download_and_get_info(url, opts)
        self._log_video_info(url, info)

    def download_audio(self, url: str) -> None:
        """Download audio only from URL."""
        self._prepare_directory(self.audio_folder)
        
        opts = {
            'extract_audio': True,
            "format": f"bestaudio[ext={audio_extension}]/b",
            'outtmpl': f'%(title)s_{self.timestamps}.%(ext)s',
            "cookiefile": "cookies_from_browser firefox"
        }
        
        info = self._download_and_get_info(url, opts)
        self._log_audio_info(info)

    def _prepare_directory(self, folder: str) -> None:
        """Create and change to target directory."""
        if not os.path.exists(folder):
            os.mkdir(folder)
        os.chdir(folder)

    def _download_and_get_info(self, url: str, opts: dict) -> dict:
        """Execute download and return info dictionary."""
        with YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=True)

    def _log_video_info(self, url: str, info: dict) -> None:
        """Log video download information."""
        video_title = info.get('title', '')
        extension = info.get('ext', '')
        raw_resolution = info.get('resolution', '')
        video_duration = info.get('duration', '')
        video_resolution = raw_resolution.split('x')[-1] or info.get('height', '')

        readable_duration = self.video_processor.convert_video_duration_from_seconds(video_duration)
        get_size = self.video_processor.convert_bytes_to_readable_format(self.timestamps)

        log_info = {
            "Video Name": f'{video_title}_{self.timestamps}.{extension}',
            "Location": f"{os.path.join(self.cwd, self.video_folder)}",
            "Duration": readable_duration,
            "Resolution": f'{video_resolution}p',
            "Size": get_size,
            "Link": url,
            "Timestamp": self.now().strftime("%A, %B %d %Y | %I:%M %p")
        }
        
        self.video_processor.log_post_download_info(log_info)
        self._print_video_success(video_title, extension, readable_duration, video_resolution, get_size)

    def _log_audio_info(self, info: dict) -> None:
        """Log audio download information."""
        audio_title = info.get('title', '')
        extension = info.get('ext', '')
        audio_duration = info.get('duration', '')

        readable_duration = self.video_processor.convert_video_duration_from_seconds(audio_duration)
        get_size = self.video_processor.convert_bytes_to_readable_format(self.timestamps, file_path=self.audio_folder)

        audio_info = {
            "Title": f'{audio_title}_{self.timestamps}.{extension}',
            "Location": f"{os.path.join(self.cwd, self.audio_folder)}",
            "Duration": readable_duration,
            "Size": get_size,
            "Timestamp": self.now().strftime("%A, %B %d %Y | %I:%M %p")
        }
        
        self.video_processor.log_post_download_info(audio_info)
        self._print_audio_success(audio_title, extension, readable_duration, get_size)

    def _print_video_success(self, title, ext, duration, resolution, size):
        """Print video download success message."""
        logging.info(f"""
Download complete!
Video name: {title}_{self.timestamps}.{ext}
Video location: {os.path.join(self.cwd, self.video_folder)}
Video duration: {duration}
Video resolution: {resolution}p
Video Size: {size}
""")

    def _print_audio_success(self, title, ext, duration, size):
        """Print audio download success message."""
        logging.info(f"""
Download complete!
Title: {title}_{self.timestamps}.{ext}
Location: {os.path.join(self.cwd, self.audio_folder)}
Duration: {duration}
Size: {size}
""")