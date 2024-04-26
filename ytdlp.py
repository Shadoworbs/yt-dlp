# This is an open source project created by shadoworbs
# Visit https://github.com/shadoworbs/yt-dlp for more information


# import the necessary modules
from resources.modules.video_downloader import download_video
from resources.modules.audio_downloader import download_audio
import yt_dlp


if __name__ == "__main__":
    # create a variable to store the link from the user
    url = input('\nEnter a youtube video link or press enter to exit: \n')
    if 'https://' in url and 'youtu' in url:
        audio_only = input('\nDo you want to download the audio only? (y/n) ')

    # check if user wants to download audio only
    if "https://" in url and 'youtu' in url and audio_only.lower() == 'y':
        download_audio(url)
    
    # download the video
    elif "https://" in url and 'youtu' in url and audio_only != 'y':

        # show available formats
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get available formats
            formats = ydl.extract_info(url, download=False)['formats']

            # Filter valid formats with resolution
            unique_resolutions = set()
            filtered_formats = []
            for format in formats:
                resolution = f"{format.get('height', '')}"
                fps = f"{format.get('fps', '')}"
                if resolution and resolution not in unique_resolutions:
                    unique_resolutions.add(resolution)
                    filtered_formats.append(format)
            # Print valid resolutions only
            if filtered_formats:
                print("\nAvailable Resolutions and Framerates:")
                print("  # Resolution    Framerate")
                print("-"*35)
                for i, format in enumerate(filtered_formats):
                    resolution = format['height']  # Use format_id for brevity
                    fps = format['fps']
                    print(f"{(i+1):2}. {str(resolution):<12}  {str(fps):<11}")
                # sys.exit()
            else:
                print("No available formats found.")
        # select video quality and fps or press enter to use the default
        # User selection
        while True:
            try:
                choice = int(input("Enter the number of the format you want to download (or 0 to cancel): "))
                if 0 <= choice <= len(formats): # Check if choice is within range and not 0
                    break
                else:
                    # if choice is not within range or is 0
                    print("Invalid choice. Please enter a number between 0 and", len(formats))
            except ValueError:
                # if user inputs a value that is not a number
                print("Invalid input. Please enter a number.")
        # set the height to selected format's height.
        video_height = filtered_formats[choice - 1]["height"]
        download_video(url, video_height)
        # fps = input('\nEnter framerate. Default is 25: ') or '25'
        
    else:
        print("\nInvalid youtube link, try again.")

