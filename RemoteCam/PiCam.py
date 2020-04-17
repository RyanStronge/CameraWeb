import os
import pyautogui as wr
import paramiko as pm
import subprocess
import random

client = pm.SSHClient()

def connect(user, host, password):
    try:
        client.set_missing_host_key_policy(pm.AutoAddPolicy())
        client.connect(host, port=22, username=user, password=password)
        if client.get_transport() is not None:
            print("Successfully Conected!")
            #print(stdout.readlines())
    except:
        print("Connection Failed!")

def checkConnection():
    if client.get_transport() is not None:
        print("Connected.")
        return True
    else:
        return False
        
def takePhotos(count):
    print("taking photos "+str(count))
    if checkConnection():
        for x in range(0, count):
            client.exec_command('cd ~/Downloads/; sudo -E python3 startup.py')
            name = "img"+str(x)
            print(name)
            path = os.getcwd()
            print(path)
            os.system('sshpass -p \'raspberry\' scp raspberrypizero.local:~/Downloads/img.jpg '+path+'/dls/'+name+'.jpg')
            client.exec_command("rm img.jpg")
            print("Running")
    else:
        print("Connect First!")

def takeSingle():
    path = os.getcwd()
    try:
        os.system("rm "+path+"/dls/single/img.jpg")
    except FileNotFoundError:
        print("File not found.")
    client.exec_command('cd ~/Downloads/; sudo -E python3 startup.py')
    print(path)
    os.system('sshpass -p \'raspberry\' scp raspberrypizero.local:~/Downloads/img.jpg '+path+'/dls/single/img.jpg')
    client.exec_command("rm ~/Downloads/img.jpg")

def takeVideos(length):
    if checkConnection():
        num = random.randint(0, 9999)
        name = "video"+str(num)+".h264"
        path = os.getcwd()
        print(path)
        client.exec_command('cd ~/Downloads; raspivid -o '+name+' -t '+(str(length)*1000))
        os.system('sshpass -p \'raspberry\' scp raspberrypizero.local:/home/pi/Downloads/video.h264 '+str(path)+'/dls/video'+str(num)+'.h264')
        client.exec_command('rm video.h264')
        print("Running")
    else:
        print("Connect First!")
