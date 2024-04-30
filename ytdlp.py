# This is an open source project created by shadoworbs
# Visit https://github.com/shadoworbs/yt-dlp for more information


# import the necessary modules
import sys
from resources.helper.video_downloader import download_video
from resources.helper.audio_downloader import download_audio
import yt_dlp


if __name__ == "__main__":
    # create a variable to store the link from the user
    url = input('\nEnter a youtube video link or press enter to exit: \n')
    if ('https://' in url 
        and 'youtu' in url
       ):
        audio_only = input('\nDo you want to download the audio only? (y/n) ')

    # check if user wants to download audio only
    if ("https://" in url 
        and 'youtu' in url 
        and audio_only.lower() == 'y'
        ):
        download_audio(url)
    
    # download the video
    elif ("https://" in url 
          and 'youtu' in url 
          and audio_only != 'y'
          ):

        # show available formats
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get available formats
            formats = ydl.extract_info(url, download=False)['formats']

            # Filter valid heihts only
            filtered_formats = []
            for format in formats:
                resolution = f"{format.get('height')}"
                fps = f"{format.get('fps')}"
                if (resolution not in filtered_formats
                    and resolution is not None
                    and resolution != 'None'
                   ):
                    filtered_formats.append(resolution) # getting rid of all duplicates and None(s)
            # show available heights (formats)
            if filtered_formats:
                print("\n[+]Available Resolutions and Framerates:")
                print(" #  Resolutions")
                print("-"*15)
                for number, height in enumerate(filtered_formats):
                    resolution = height
                    print(f"{(number+1):2}. {str(resolution):<12}")
                # sys.exit()

            else:
                print("No available formats found.")
        # select video quality (height)
        while True:
            try:
                choice = int(input("Enter the number of the format you want to download (or 0 to cancel): "))
                if 1 <= choice <= len(filtered_formats): # Check if choice is within range and not 0
                    break
                elif int(choice) == 0:
                    sys.exit()
                else:
                    # if choice is not within range or is 0
                    print("Invalid choice. Please enter a number from 1 to", len(filtered_formats))
            except ValueError:
                # if user inputs a value that is not a number
                print("Invalid input. Please enter a number.")
        # set the height to selected format's height.
        video_height = filtered_formats[choice - 1]
        download_video(url, video_height)
        # fps = input('\nEnter framerate. Default is 25: ') or '25'
        
    else:
        print("\nInvalid youtube link, try again.")

