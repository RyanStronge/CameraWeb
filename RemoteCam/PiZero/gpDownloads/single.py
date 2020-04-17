import os
import sys
# Import GoPro library
from goprocam import GoProCamera, constants
# Initialise GoPro
gp = GoProCamera.GoPro()
# Take photo with GoPro with 0 second delay
gp.take_photo(0)
# Save file name as single.jpg
gp.downloadLastMedia(custom_filename="single.jpg")
print("Downloading")
