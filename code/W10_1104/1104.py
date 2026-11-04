from flask import Flask, render_template, redirect, url_for, jsonify
import RPi.GPIO as GPIO 
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(18, GPIO.IN)
state_motion = {"state_mo" : "Not Oprating"}
app = Flask(__name__)
count = 0

#  def Operator(GPIO, state_motion): << power point 6 ver.
def Operator():  # Prof. ver.
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(18, GPIO.IN)

    global count

    while True:
        if GPIO.input(18) == True:
            count += 1
            print("Detect!", count)
            state_motion["state_mo"] = "Motion Detect"
            GPIO.output(21, True)
            sleep(0.3)
        
        if GPIO.input(18) == False:
            state_motion["state_mo"] = "Motion Nothing"
            GPIO.output(21, False)

# prof. ver.
def close_op(GPIO):
    GPIO.cleanup()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start")   
def start():
    Operator()
    return redirect(url_for("home"))

@app.route("/reset")   
def reset():
    global count
    count = 0
    return redirect(url_for("home"))

@app.route("/state")
def get_state():
    return jsonify({"state" : state_motion["state_mo"]})

# power point 6 ver.
"""    
def close_op(GPIO):
    GPIO.cleanup()
    
@app.route("/state")
def get_state():
    return jsonify({"state" : state_motion["state_mo"]})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/on")   
def led_on():
    Operator(GPIO, state_motion)
    return redirect(url_for("home"))

@app.route("/off")
def led_off():
    GPIO.cleanup()
    state_motion["state_mo"] = "Not Operating"
    close_op(GPIO)
    return redirect(url_for("home"))
"""
if __name__ == "__main__" :
    try:
        app.run(host="192.168.1.116" , port=8000)
    finally:
        GPIO.cleanup()
        close_op(GPIO)
