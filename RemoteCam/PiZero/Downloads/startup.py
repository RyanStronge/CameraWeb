# importing PiCamera
from picamera import PiCamera
import os
import sys
# Initialise PiCam
camera = PiCamera()
# Take photo with PiCam
camera.capture('img.jpg')
