from flask import Flask, render_template, redirect, url_for
import RPi.GPIO as GPIO
# from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)

pwm = GPIO.PWM(21, 3000)
pwm.start(0)
duty = 0

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/on")
def led_on():
    global duty
    pwm.ChangeDutyCycle(duty)
    duty = duty + 20
    if(duty >= 100):
        duty = 100
    return redirect(url_for("home"))

@app.route("/off")
def led_off():
    global duty
    pwm.ChangeDutyCycle(duty)
    duty = duty - 20
    if(duty <= 0):
        duty = 0
    return redirect(url_for("home"))

if __name__ == "__main__":
    try:
        app.run(host="192.168.1.116", port=8000)
    finally:
        GPIO.cleanup()