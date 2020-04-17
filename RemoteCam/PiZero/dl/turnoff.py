import os
import sys
from goprocam import GoProCamera, constants

# turn off GoPro
gp = GoProCamera.GoPro()
gp.power_off()
print("Power Off")
