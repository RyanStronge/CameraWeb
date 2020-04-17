from picamera import PiCamera
#import picam
from time import sleep
import os
import sys

# get number of photos to take from picam call eg.   python3 piCamTakePhotos.py 5
num = sys.argv[1]
# initialise PiCamera
camera = PiCamera()

# Take this number of photos using for loop
for x in range(0, int(num)):
    camera.start_preview()
    camera.capture('piPicture.jpg')
    os.system("sudo scp piPicture.jpg pi@raspberrypi.local:~/imgs")
    os.remove("piPicture.jpg")
print("Took and downloaded " + num + " pictures!")

