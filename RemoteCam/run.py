from flask import Flask, render_template, redirect, url_for, request, Response, flash
from flask import make_response
from camera_pi import Camera
from base_camera import BaseCamera

app = Flask(__name__)
import GoPro as gp
import PiCam as p

@app.route('/')
def index():
    gp.connect("pi", "raspberrypizero.local", "raspberry")   
    print(gp.checkConnection())
    if gp.checkConnection():
        if gp.checkGPConnection():
            return render_template('index.html')
        else: return render_template('error.html', error="Check GoPro Connection!" )
    else: return render_template('error.html', error="Check Pi Zero Connection for SSH!")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'+ frame + b'\r\n')

@app.route('/picam')
def picam():
    print("Running")
    return render_template('picam.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream')
def stream():
    if gp.checkConnection():
        quality = request.args.get('quality', type=str)
        ip = "0.0.0.0:5000"
        gp.stream(quality, ip) 
        print("ok")   
        return 'OK'
    return flash("Connection Error")
@app.route('/takePhotos')
def takePhotos():
    if gp.checkConnection():
        print(gp.checkConnection())
        count = request.args.get('count', type=int)
        gp.takePhotos(count)
        flash("Taking "+count+" photos!")
        return 'OK'
    else:
        print("connection errors")
        flash("Connection Error!")
        return 'Check Connection'

@app.route('/PtakePhotos')
def PtakePhotos():
    if gp.checkConnection():
        count = request.args.get('Pcount', type=int)
        p.takePhotos(count)
        return 'OK'
    return 'Connection Error'

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
    return 'OK'


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
    if gp.checkConnection():
        length = request.args.get('PcaptureLength', type=int)
        print("length: "+str(length))
        p.takeVideos(str(length))
        return 'OK'
    return 'Connection Error'

@app.route('/res')
def res():
    if gp.checkConnection():
        choice = request.args.get('res', type=str)
        print(choice)

       
        gp.changeResolution(choice)
    
        return 'OK'
            
if __name__ == "__main__":
    app.secret_key = 'w77pebv6'
    app.run(debug=True, host='0.0.0.0')