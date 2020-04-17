from flask import Flask, render_template, redirect, url_for, request, Response, flash, send_file, Response, after_this_request
from flask import make_response
from camera_pi import Camera
from base_camera import BaseCamera
import os
import zipfile
import io
import pathlib
import glob
import time
import requests
import shutil
import time

app = Flask(__name__)
import GoPro as gp
import PiCam as p

def sendFile(fileName): #input should be like img0.jpg
    os.getcwd()
    #path = os.getcwd+'/dls/'+fileName
    return send_file(fileName, attachment_filename=fileName, as_attachment=True)


@app.route('/')
def index():
    gp.connect("pi", "raspberrypizero.local", "raspberry")   
    print(gp.checkConnection())
    if gp.checkConnection():
        if gp.checkGPConnection():
            return render_template('index.html')
        else: return render_template('error.html', error="Check GoPro Connection!" )
    else: return render_template('error.html', error="Check Pi Zero Connection for SSH!")


@app.route('/picam')
def picam():
    p.connect("pi", "raspberrypizero.local", "raspberry")   
    print(p.checkConnection())
    if p.checkConnection():
        return render_template('picam.html')
    else:
        return render_template('error.html', error="Check Pi Zero Connection for SSH!")

@app.route('/single')
def single():
    try:
        os.system("rm "+os.getcwd()+"/dls/single/single.jpg")
    except FileNotFoundError:
        print("File not found.")
    gp.connect("pi","raspberrypizero.local","raspberry")
    if gp.checkConnection():
        print("connection ok")
        gp.takeOne()
        path = os.getcwd()
        return send_file(path+"/dls/single/single.jpg", as_attachment=True, cache_timeout=0)
    else:
        return render_template('error.html', error="Check GoPro Connection!")

@app.route('/pSingle')
def pSingle():
    p.connect("pi", "raspberrypizero.local","raspberry")
    if p.checkConnection():
        print("connection ok")
        p.takeSingle()
        path = os.getcwd()
        return send_file(path+"/dls/single/img.jpg", as_attachment=True, cache_timeout=0)
    else:
        return render_template('error.html', error="Check PiCam Connection!")

@app.after_request
def add_header(r):
    print("bye cache")
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

    





@app.route('/takePhotos')
def takePhotos():
    if gp.checkConnection():
        count = request.args.get('count', type=int)
        gp.takePhotos(count)
        return 'OK'
    else:
        return render_template('error.html', error="Check GoPro Connection for SSH!")

@app.route('/PtakePhotos')
def PtakePhotos():
    print("taking photos run.py")
    if p.checkConnection():
        count = request.args.get('count', type=int)
        p.takePhotos(count)
        return 'OK'
    else:
        return render_template('error.html', error="Check PiCam Connection for SSH!")

@app.route('/checkConnection')
def checkConnection():
    print(gp.checkConnection())
    if not gp.checkConnection():
        return render_template('error.html')
    else:
        return 'ok'




@app.route('/turnon')
def turnOn():
    gp.turnOn()
    return 'OK' 

@app.route('/turnoff')
def turnOff():
    gp.turnOff()
    return 'OK'

@app.route('/downloadAll')
def downloadAll(): 
    gp.downloadAll()
    dls = str(os.getcwd())+"/dls/data.zip"
    baseDir = os.getcwd()
    print(dls)
    result = send_file(dls, as_attachment=True)
    try:
        shutil.rmtree(os.getcwd()+'/dls')
        os.system("cd "+baseDir+"; mkdir dls")
    except Exception as error:
        print("Error deleting files")
        print(error) 
    print("returning file.")
    return result

@app.route('/connect')
def connect():
    gp.connect("pi", "raspberrypizero.local", "raspberry")
    if(gp.checkConnection()):
        return 'OK'
    return 'Connection Error'

@app.route('/record')
def record():
    if gp.checkConnection():
        length = request.args.get('captureLength', type=int)
        print("length: "+str(length))
        gp.record(str(length))
        return 'OK'
    return 'Connection Error'

@app.route('/Precord')
def Precord():
    if p.checkConnection():
        print("route")
        length = request.args.get('captureLength', type=int)
        print("length: "+str(length))
        p.takeVideos(str(length))
        return 'OK'
    return render_template('error.html', error="Connection error!")

@app.route('/res')
def res():
    if gp.checkConnection():
        choice = request.args.get('res', type=str)
        print(choice)

       
        gp.changeResolution(choice)
    
        return 'OK'
            
if __name__ == "__main__":
    print(os.getuid())
    os.setuid(1000)
    print(os.getuid())
    app.secret_key = 'w77pebv6'
    app.run(debug=True, host='0.0.0.0')
