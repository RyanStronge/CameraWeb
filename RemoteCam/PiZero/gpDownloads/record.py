import os
import sys
from goprocam import GoProCamera, constants

length = sys.argv[1]
gp = GoProCamera.GoPro()
gp.shoot_video(int(length))
gp.downloadLastMedia(custom_filename="video.mp4")
print(length + " seconds of video recording")
print("Downloading")
