from flask import Flask, render_template, redirect, url_for
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)


app = Flask(__name__) # Flask() is class

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/but")
def button():
    try:
        while True:
            GPIO.output(21,True)
            sleep(0.5)
            GPIO.output(21, False)
            sleep(0.5)
    
    except KeyboardInterrupt:
        GPIO.cleanup()
    
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="192.168.1.116", port=5000)
