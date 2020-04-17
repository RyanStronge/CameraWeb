import os
import sys
# Import GoPro
from goprocam import GoProCamera, constants
# Initialise GoPro
gp = GoProCamera.GoPro()
# Take Photo with 0 second delay
gp.take_photo(0)
# Save photo just taken with filename img.jpg
gp.downloadLastMedia(custom_filename="img.jpg")
print("Downloading")
