import os
import sys
from goprocam import GoProCamera, constants
gp = GoProCamera.GoPro()
gp.take_photo(0)
gp.downloadLastMedia(custom_filename="img.jpg")
print("Downloading")
