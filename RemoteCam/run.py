import PiCam as p
import GoPro as gp
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

# Initialise Flask app.
app = Flask(__name__)


def sendFile(fileName):  # input should be like img0.jpg
    os.getcwd()
    # sends flask file to user on webpage
    return send_file(fileName, attachment_filename=fileName, as_attachment=True)

# when user goes onto website, connects them to the GoPro and if it's connected, returns the GoPro index.html page, otherwise returns an error message
@app.route('/')
def index():
    gp.connect("pi", "raspberrypizero.local", "raspberry")
    print(gp.checkConnection())
    if gp.checkConnection():
        if gp.checkGPConnection():
            return render_template('index.html')
        else:
            return render_template('error.html', error="Check GoPro Connection!")
    else:
        return render_template('error.html', error="Check Pi Zero Connection for SSH!")

# tries to connected to PiCam and if it's connected, returns the requested webpage, otherwise returns an error message
@app.route('/picam')
def picam():
    p.connect("pi", "raspberrypizero.local", "raspberry")
    print(p.checkConnection())
    if p.checkConnection():
        return render_template('picam.html')
    else:
        return render_template('error.html', error="Check Pi Zero Connection for SSH!")

# try to remove file if it exists, connect to gopro, if it's connected, take a single photo and return it to the user.
@app.route('/single')
def single():
    try:
        os.system("rm "+os.getcwd()+"/dls/single/single.jpg")
    except FileNotFoundError:
        print("File not found.")
    gp.connect("pi", "raspberrypizero.local", "raspberry")
    if gp.checkConnection():
        print("connection ok")
        gp.takeOne()
        path = os.getcwd()
        return send_file(path+"/dls/single/single.jpg", as_attachment=True, cache_timeout=0)
    else:
        return render_template('error.html', error="Check GoPro Connection!")

# Same as above except with PiCam
@app.route('/pSingle')
def pSingle():
    p.connect("pi", "raspberrypizero.local", "raspberry")
    if p.checkConnection():
        print("connection ok")
        p.takeSingle()
        path = os.getcwd()
        return send_file(path+"/dls/single/img.jpg", as_attachment=True, cache_timeout=0)
    else:
        return render_template('error.html', error="Check PiCam Connection!")

# Clear cache after making a request because sometimes it would cause the wrong file to be returned.
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# if gopro is connected, get variable from URL and feed it into the takePhotos function. If not connected, return an error message.
@app.route('/takePhotos')
def takePhotos():
    if gp.checkConnection():
        count = request.args.get('count', type=int)
        gp.takePhotos(count)
        return 'OK'
    else:
        return render_template('error.html', error="Check GoPro Connection for SSH!")

# Same as above, except for PiCam.
@app.route('/PtakePhotos')
def PtakePhotos():
    print("taking photos run.py")
    if p.checkConnection():
        count = request.args.get('count', type=int)
        p.takePhotos(count)
        return 'OK'
    else:
        return render_template('error.html', error="Check PiCam Connection for SSH!")

# Return error.html if GoPro is not connected, or else return 'ok'.
@app.route('/checkConnection')
def checkConnection():
    print(gp.checkConnection())
    if not gp.checkConnection():
        return render_template('error.html')
    else:
        return 'ok'

# Call GoPro turnOn function.
@app.route('/turnon')
def turnOn():
    gp.turnOn()
    return 'OK'

# Call GoPro turnOff function.


@app.route('/turnoff')
def turnOff():
    gp.turnOff()
    return 'OK'

# Download all files from GoPro.
@app.route('/downloadAll')
def downloadAll():
    gp.downloadAll()
    # Download location
    dls = str(os.getcwd())+"/dls/data.zip"
    baseDir = os.getcwd()
    print(dls)
    # Prepare send_file
    result = send_file(dls, as_attachment=True)
    try:
        # Remove /dls folder.
        shutil.rmtree(os.getcwd()+'/dls')
        os.system("cd "+baseDir+"; mkdir dls")
    except Exception as error:
        print("Error deleting files")
        print(error)
    print("returning file.")
    # Return folder.
    return result


@app.route('/connect')
def connect():
    # Connect to GoPro.
    gp.connect("pi", "raspberrypizero.local", "raspberry")
    if(gp.checkConnection()):
        return 'OK'
    return 'Connection Error'

# Gets recording length from URL and feeds it into the recording video function for GoPro.
@app.route('/record')
def record():
    if gp.checkConnection():
        length = request.args.get('captureLength', type=int)
        print("length: "+str(length))
        gp.record(str(length))
        return 'OK'
    return 'Connection Error'


# Same as above except for PiCam.
@app.route('/Precord')
def Precord():
    if p.checkConnection():
        print("route")
        length = request.args.get('captureLength', type=int)
        print("length: "+str(length))
        p.takeVideos(str(length))
        return 'OK'
    return render_template('error.html', error="Connection error!")

# Get resolution from URL and feed it into the changeResolution GoPro choice.
@app.route('/res')
def res():
    if gp.checkConnection():
        choice = request.args.get('res', type=str)
        print(choice)
        gp.changeResolution(choice)
        return 'OK'


# Sets UID to 1000.
if __name__ == "__main__":
    os.setuid(1000)
    app.secret_key = 'w77pebv6'
    app.run(debug=True, host='0.0.0.0')
