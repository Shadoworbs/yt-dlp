# This is an open source project created by shadoworbs
# Visit https://github.com/shadoworbs/yt-dlp for more information


# import the necessary modules
import sys
from helper.downloaders import download_video, download_audio
import yt_dlp

def main():
# create a variable to store the link from the user
    url = input('\nEnter a youtube video link or press enter to exit: \n')
    if ('https://' in url 
        and 'youtu' in url
       ):
        audio_only = input('\nDo you want to download the audio only? (y/n) \n')

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
                choice = int(input("Enter the number of the resolution you want to download (or 0 to cancel): "))
                if 1 <= choice <= len(filtered_formats): # Check if choice is within range and not 0
                    break
                elif int(choice) == 0:
                    sys.exit()
                else:
                    # if choice is not within range or is 0
                    print(f"Invalid choice. Please enter a number from 1 to {len(filtered_formats)}\n")
            except ValueError:
                # if user inputs a value that is not a number
                print("Invalid input. Please enter a number.\n")
        # set the height to selected format's height.
        video_height = filtered_formats[choice - 1]
        download_video(url, video_height)
    elif 'https' not in url and 'youtu' not in url and len(url) >= 1:
        print("\nInvalid youtube link, try again.\n")
    else:
        sys.exit(0)

## initiate the download https://youtube.com/shorts/n-Rf3EJ_WaU?si=vMwAAWI7QlkT4IYr
if __name__ == "__main__":
    main()

