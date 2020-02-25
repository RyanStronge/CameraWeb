import os
import pyautogui as wr
import paramiko as pm

client = pm.SSHClient()

""" def turnOn():
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 turnOn.py'
        print(command)
        client.exec_command(command)
        print("Running")
    else:
        print("Please Connect First!") """


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
    print("Check GoPro Conection! Current WiFi network is: ")
    stdout = client.exec_command('iwgetid')
    print(stdout)
    return False

def takePhotos(count):
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 PtakePhotos.py '+str(count)
        print(command)
        client.exec_command(command)
        print("Running")
    else:
        print("Connect First!")

def takeVideos(length):
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 PtakeVideos.py '+str(length)
        print(command)
        client.exec_command(command)
        print("Running")
    else:
        print("Connect First!")
