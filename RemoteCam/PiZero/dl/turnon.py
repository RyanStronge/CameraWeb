import os
import sys
from goprocam import GoProCamera, constants

# Turn on GoPro
gp = GoProCamera.GoPro()
gp.power_on("d4-d9-19-9c-54-8e")  # Have to use MAC address as parameter.
print("Turning on")
