import sys
from goprocam import GoProCamera, constants  # import gopro library
# initialise GoPro
gp = GoProCamera.GoPro()
# get resolution choice from system arg eg. in terminal:    python3 changeResolution.py '4k'
choice = sys.argv[1]
# set GoPro to entered resolution.
gp.video_settings((choice))
print("Resolution changed")
