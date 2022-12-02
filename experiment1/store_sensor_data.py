import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
from micropython import const
import serial
import re
import json


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

def download_model(finger):
    _REGMODEL = const(0x05)
    finger._send_packet([_REGMODEL])
    if finger._get_packet(12)[0] == 0:
        res = finger._get_data(9)
    return res


uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

filename = input("enter filename : ")

template = False

fingerimg = 1 # Slot to store the fingerprint data
outputs = []
for _ in range(6):
    state = True
    while state:
        print("reading print")
        i = finger.get_image()
        print(i)
        time.sleep(1)
        print("read print ..... ")
        if i == adafruit_fingerprint.OK:
            print("Image taken")
            state = False
        elif i == adafruit_fingerprint.NOFINGER:
            print("- No finger .")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
            exit() # return False
        else:
            print("Other error")
            exit() #return False
    if template:
        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print(i)
                print("Other error")
            exit()
    data = bytearray(256)
    out = finger.get_fpdata(sensorbuffer = "image", slot=fingerimg)
    outputs.append(out)
    print("Sensor Results: " ,out)
    # print("Finger print: ", data)
# Once loaded all the images
with open(filename + ".json", 'w') as f:
    f.write(json.dumps(outputs))
print(f"File saved in {filename}_{template}.json ...")

