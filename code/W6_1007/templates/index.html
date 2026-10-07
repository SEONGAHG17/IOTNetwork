from flask import Flask, render_template, redirect, url_for
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIO setting
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW) # when playing starting, LED is OFF

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/on")
def led_on():
    GPIO.output(21, GPIO.HIGH) # turn on the LED
    return redirect(url_for("home")) 

@app.route("/off")
def led_off():
    GPIO.output(21, GPIO.LOW) # turn off the LED
    return redirect(url_for("home")) 


if __name__ == "__main__":
    try:
        app.run(host="192.168.1.116", port=8000)
    
    finally:
        GPIO.cleanup()
