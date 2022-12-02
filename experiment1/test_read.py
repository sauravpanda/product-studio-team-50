import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

import serial
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

while True:
    print("reading print")
    i = finger.get_image()
    print(i)
    time.sleep(1)
    print("read print ..... ")
    if i == adafruit_fingerprint.OK:
        print("Image taken")
        break
    if i == adafruit_fingerprint.NOFINGER:
        print("- No finger .")
    elif i == adafruit_fingerprint.IMAGEFAIL:
        print("Imaging error")
        exit() # return False
    else:
        print("Other error")
        exit() #return False
