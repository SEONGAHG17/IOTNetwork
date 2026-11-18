from flask import Flask, render_templete, redirect, url_for, jsonify
import RPi.GPIO as GPIO
import time

TRIG_PIN = 20
ECHO_PIN = 21
state_dict = {"state_distance" : 0}

app = Flask(__name__)

def initUltrasonic():
    GPIO.setwarnings (False)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def controlUltrasonic():
    distance = 0.0
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.5)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)
    return distance

def main():
    GPIO.setmode(GPIO.BCM)
    distance = 0.0
    initUltrasonic()
    print("Ultrasonic Operationg ...")
    try:
        while True:
            distance = controlUltrasonic()
            state_dict["state_distance"] = str(distance)
            print("distance : %.2f cm" %distance)
    except KeyboardInterrupt:
        GPIO.cleanup()

# if __name__ == '__main__':
#     main()



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/on")
def on():
    main()
    return redirect(url_for("home")) 

@app.route("/off")
def reset():
    return redirect(url_for("home")) 

@app.route("/state")
def send_state():
    return jsonify({"state_data" : state_dist["state_distance"]})



if __name__ == "__main__":
    try:
        app.run(host = "192.168.1.116", port=5000)
    finally:
        GPIO.cleanup()