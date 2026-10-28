from flask import Flask, render_template, redirect, url_for, jsonify
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)

pwm = GPIO.PWM(21, 50) # servo moter Basic Set

pwm.start(0)
app = Flask(__name__)

def set_forward_speed():
    print("Foward Increment speed")
    for duty in range(8, 12):
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.6)

def set_backward_speed():
    print("backward Increment speed")
    for duty in range(7, 3, -1):
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.6)

def stop_speed():
    print("Stop")
    pwm.ChangeDutyCycle(7.5)
    time.sleep(1)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/forward")
def forward():
    set_forward_speed()
    return redirect (url_for("home"))

@app.route("/backward")
def backward():
    set_backward_speed()
    return redirect (url_for("home"))

@app.route("/stop")
def stop():
    stop_speed()
    return redirect (url_for("home"))

if __name__ == "__main__":
    try:
        app.run(host = "192.168.1.116", port = 8000)
        # why port = 8000? 
        # because C320 WIFI setting is 8000
    finally:
        pwm.stop()
        GPIO.cleanup()