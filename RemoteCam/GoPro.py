import os
import pyautogui as wr
import paramiko as pm
import time
import shutil
import random as r

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

def make_archive(source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        print(source, destination, archive_from, archive_to)
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)


def checkGPConnection():
        print("connection ok")
        chan = client.invoke_shell()
        chan.sendall('iwgetid\r\n')
        time.sleep(0.9)
        output = chan.recv(4096)
        print(output)
        if "RoboticArmGoPro" in str(output):
            print("GoPro network is: "+ str(output))
            return True
        return False

def turnOff():
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 turnOff.py'
        print(command)
        client.exec_command(command)
        print("Running")
    else:
        print("Please Connect First!")

def turnOn():
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 turnOn.py'
        print(command)
        client.exec_command(command)
        print("Running")
    else:
        print("Please Connect First!")
    

def stream(quality, ip):
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 stream.py '+quality + ' '+ip
        print(command)
        client.exec_command(command)
        print("Running")
    else:
        print("Please Connect First!")

def takePhotos(captureCount):
    print(captureCount)
    for x in range(0, captureCount):
        client.exec_command('cd ~/gpDownloads; sudo -E python3 piGoPro.py')
        name = "gpImg"+str(x)
        print(name)
        path = os.getcwd()
        os.system('sshpass -p \'raspberry\' scp raspberrypizero.local:~/gpDownloads/img.jpg '+path+'/dls/'+name+'.jpg') 
        client.exec_command("cd ~/gpDownloads; rm img.jpg")
        print("Running GP Image")   

def takeOne():
    client.exec_command('cd ~/gpDownloads; sudo -E python3 single.py')
    path = os.getcwd()
    os.system('sshpass -p \'raspberry\' scp raspberrypizero.local:~/gpDownloads/single.jpg '+path+'/dls/single/single.jpg')
    client.exec_command('rm ~/gpDownloads/single.jpg') 


def record(captureLength):
    command = 'cd ~/gpDownloads; pwd; sudo -E python3 record.py '+str(captureLength)
    print(command)
    client.exec_command(command)
    vName = "video"+ str(r.randint(0, 9999))
    print(vName)
    vPath = os.getcwd()
    os.system('sshpass -p \'raspberry\' scp raspberrypizero.local:~/gpDownloads/video.mp4 '+vPath+'/dls/'+vName+'.mp4') 
    client.exec_command("cd ~/gpDownloads; rm video.mp4")
    print("Running GP Video")

def downloadAll():
    dls = str(os.getcwd())+"/dls"
    print(dls)
    make_archive(dls, dls+'/data.zip')

def changeResolution(choice):
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 changeResolution.py '+str(choice)
        print(command)
        client.exec_command(command)
        print("Running")
    else:
        print("Please Connect First!") 