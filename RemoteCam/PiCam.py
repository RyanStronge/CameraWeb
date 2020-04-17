import os
import paramiko as pm
import subprocess
import random

client = pm.SSHClient()

# Connect to PiZero using SSH.


def connect(user, host, password):
    try:
        client.set_missing_host_key_policy(pm.AutoAddPolicy())
        client.connect(host, port=22, username=user, password=password)
        if client.get_transport() is not None:
            # If SSH successful...
            print("Successfully Conected!")
    except:
        print("Connection Failed!")

# Checks if connection to Pi Zero is stable and returns true/false based on response.
def checkConnection():
    if client.get_transport() is not None:
        print("Connected.")
        return True
    else:
        return False

# Takes a number of photos that the user has specified, use scp to send it to the Pi 3B and remove it from Pi Zero
def takePhotos(count):
    print("taking photos "+str(count))
    if checkConnection():
        for x in range(0, count):
            client.exec_command('cd ~/Downloads/; sudo -E python3 startup.py')
            name = "img"+str(x)
            print(name)
            path = os.getcwd()
            print(path)
            os.system(
                'sshpass -p \'raspberry\' scp raspberrypizero.local:~/Downloads/img.jpg '+path+'/dls/'+name+'.jpg')
            client.exec_command("rm img.jpg")
            print("Running")
    else:
        print("Connect First!")

# Takes a single photo, use scp to send it to the Pi 3B and remove it from Pi Zero
def takeSingle():
    path = os.getcwd()
    try:
        os.system("rm "+path+"/dls/single/img.jpg")
    except FileNotFoundError:
        print("File not found.")
    client.exec_command('cd ~/Downloads/; sudo -E python3 startup.py')
    print(path)
    os.system('sshpass -p \'raspberry\' scp raspberrypizero.local:~/Downloads/img.jpg ' +
              path+'/dls/single/img.jpg')
    client.exec_command("rm ~/Downloads/img.jpg")

# Takes a video of length that the user has specified, save it as a random name using a random number generator, use scp to send it to the Pi 3B and remove it from Pi Zero
def takeVideos(length):
    if checkConnection():
        num = random.randint(0, 9999)
        name = "video"+str(num)+".h264"
        path = os.getcwd()
        print(path)
        client.exec_command('cd ~/Downloads; raspivid -o ' +
                            name+' -t '+(str(length)*1000))
        os.system('sshpass -p \'raspberry\' scp raspberrypizero.local:/home/pi/Downloads/video.h264 ' +
                  str(path)+'/dls/video'+str(num)+'.h264')
        client.exec_command('rm video.h264')
        print("Running")
    else:
        print("Connect First!")
