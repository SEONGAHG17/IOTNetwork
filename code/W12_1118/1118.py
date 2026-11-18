import spidev
from time import sleep

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000  # 1 Mhz
spi.mode = 3
WATER_CHANNER = 0

def readAnalog(channel):
    r = spi.xfer2([1, (8 + channel) << 4.0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out

while True:
    voltage = readAnalog(0) * 3.3/1024
    print(voltage)
    sleep(1)
