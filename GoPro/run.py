from flask import Flask, render_template, redirect, url_for, request
from flask import make_response

app = Flask(__name__)
import GoPro as gp

@app.route('/')
def index():
    
    gp.connect("pi", "raspberrypizero.local", "raspberry")   
    print(gp.checkConnection())
    return render_template('index.html')
    
@app.route('/takePhotos')
def takePhotos():
    if gp.checkConnection():
        count = request.args.get('count', type=int)
        gp.takePhotos(count)
        return 'OK'
    return 'Connection Error'

@app.route('/checkConnection')
def checkConnection():
    gp.checkConnection
    return 'OK'

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

@app.route('/res')
def res():
    if gp.checkConnection():
        choice = request.args.get('res', type=str)
        print(choice)

       
        gp.changeResolution(choice)
    
        return 'OK'
            
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')