import os
import sys
# Import GoPro library
from goprocam import GoProCamera, constants
# Get  recording length from argument eg. python3 record.py 10     would mean record for 10 seconds.
length = sys.argv[1]
# Initialise GoPro
gp = GoProCamera.GoPro()
# Take video of argument length in seconds
gp.shoot_video(int(length))
# Save video just taken as name video.mp4
gp.downloadLastMedia(custom_filename="video.mp4")
print(length + " seconds of video recording")
print("Downloading")
