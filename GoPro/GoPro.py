import os
import pyautogui as wr
import paramiko as pm

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
    print("Check GoPro Conection! Current WiFi network is: ")
    stdin, stdout, stderr = client.exec_command('iwgetid')
    print(stdout)
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
    

def takePhotos(captureCount):
    if checkConnection():
        stdin, stdout, stderr = client.exec_command('cd /boot; pwd; sudo -E python3 piGoPro.py '+str(captureCount))
        print("Running")
    else:
        print("Please Connect First!")

def record(captureLength):
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 record.py '+str(captureLength)
        print(command)
        client.exec_command(command)
        print("Running")
    else:
        print("Please Connect First!")

def downloadAll():
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 downloadAll.py'
        client.exec_command(command)
        print("Running")
    else:
        print("Please Connect First!")

def changeResolution(choice):
    if checkConnection():
        command = 'cd /boot; pwd; sudo -E python3 changeResolution.py '+str(choice)
        print(command)
        client.exec_command(command)
        print("Running")
    else:
        print("Please Connect First!")




    

    


    

        
    

 