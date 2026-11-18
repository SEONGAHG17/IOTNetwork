from flask import Flask, render_template, redirect, url_for, jsonify
import spidev
from time import sleep

val_water = {"water_val" : "0"}
app = Flask(__name__)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
spi.mode = 3
WATER_CHANNEL = 0

def readAnalog(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out

def main():
    while True:
        voltage = readAnalog(WATER_CHANNEL) * 3.3/1024
        val_water["water_val"] = str(voltage)
        print(voltage)
        sleep(1)
    return redirect(url_for("home"))


@app.route("/water")
def get_water():
    return jsonify({"water" : val_water["water_val"]})


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/on")
def water_on():
    main()
    return redirect(url_for("home"))

@app.route("/off")
def water_off():
    val_water["water_val"] = "0"
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="192.168.1.116", port=8000)