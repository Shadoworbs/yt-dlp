"""
Configuration file for the helper functions
"""
# Select the video extension you want to download eg. mp4, mkv, webm, etc. default is mkv
video_merge_output_format = "mkv" # this will be the extension of the video after merging


# Select the video format selection options (height, fps) for the video to be downloaded
# DON'T EDIT THIS UNLESS YOU KNOW WHAT YOU'RE DOING
video_format_selection_options = "((bv*[ext=mp4])[height<={}]/(wv*[ext=mp4]/wv*)) + (ba[ext=mp3]/ba) / (b[fps<={}]/b)[height<={}]/(w[fps<={}]/w)"

# TODO: More stuff will be added here soon
