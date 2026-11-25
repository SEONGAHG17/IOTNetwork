from flask import Flask, render_template, redirect, url_for, jsonify
import RPi.GPIO as GPIO
import time
import board
import adafruit_dht

app = Flask(__name__)

val_TH = {"temp_val" : "0", "humid_val":"0"}
TempHumid = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

temp = "0"
humid = "0"
dhtDevice = adafruit_dht.DHT11(board.D4)

def main():

    while True:
        if(TempHumid == False):
            val_TH["temp_val"] = "0"
            val_TH["humid_val"] = "0"
            break

        temp = dhtDevice.temperature
        humid = dhtDevice.humidity
        val_TH["temp_val"] = str(temp)
        val_TH["humid_val"] = str(humid)

        print("Temptation = {:.3f}".format(temp))
        print("Humid = {:.3f}".format(humid))
        time.sleep(0.5)

@app.route("/th")
def TempHum():
    return jsonify({"temp" : val_TH["temp_val"],"humid" : val_TH["humid_val"] })        

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/on")
def led_on():
    global TempHumid
    TempHumid = True
    main()
    GPIO.output(21, True)
    return redirect(url_for("home"))

@app.route("/off")
def led_off():
    global TempHumid
    TempHumid = False
    GPIO.output(21, False)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="192.168.1.116", port=8000)
