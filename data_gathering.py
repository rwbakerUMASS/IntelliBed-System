print("Loading Libraries...")
from tkinter import Y

from hx711 import HX711
from firebase import Firebase
import RPi.GPIO as GPIO
import time
import numpy as np
from plotXY import plot
from firebase_config import CONFIG
import json

#   LAYOUT OF SENSORS
#   yellow(3)   green(2)
#   red(1)      blue(0)

def getXY(values):
    #x=ratio of left and right
    #y=ratio of top and bottom
    total = np.sum(values)
    #handle divide by 0
    total += 1e-9
    x=(values[0]+values[2])/(total)
    y=(values[2]+values[3])/(total)
    return x,y

def calibrateSensors(sensors,num_samples):
    input("Add weight to center of bed")
    print("Finding Base Scalars...")
    for hx in sensors:
        vals=[]
        hx.set_reference_unit(1)
        for i in range(num_samples):
            vals.append(hx.get_weight(5))
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
        mean=np.mean(vals)
        print("Base = ",mean)
        hx.set_reference_unit(mean)

def write_to_json(data):
    with open("data.json", "r+") as f:
        try:
            f_data = json.load(f)
        except json.decoder.JSONDecodeError:
            f_data = {}
        for key in data:
            if 'data' not in f_data.keys():
                f_data['data']={}
            f_data['data'][key]=data[key]
        f.seek(0)
        json.dump(f_data, f, indent=4)
        f.close()

def main():
    fb = Firebase(CONFIG())

    clear = input("Clear Firebase? (y/n): ")
    if clear.lower()=='y':
        fb.clearTable()

    GPIO.setwarnings(False)
    print("Initializing HX711s...")
    sensors = [HX711(20,21),HX711(12,16),HX711(17,27),HX711(5,6)]
    print("Setting HX711 Reading Format...")
    print("Taring Scales...")
    for hx in sensors:
        hx.set_reading_format("MSB", "MSB")
        hx.reset()
        hx.tare()
    calibrateSensors(sensors,5)
    classification = input("Input activity: ")

    data = {}

    while True:
        try:
            timestamp=str(time.time()).replace(".","-")
            vals = []
            for hx in sensors:
                vals.append(max(0,hx.get_weight(1)))
                hx.power_down()
                hx.power_up()
            x,y = getXY(vals)
            data[timestamp]={"class":classification,"data":{"sensor":vals,"X":x,"Y":y}}
            # plot(x,y)
            print('X:',x,' Y:',y)
            time.sleep(0.05)
        except(KeyboardInterrupt):
            print("\nData Collection Ended")
            write = input("Write Data? (y/n):")
            if write.lower()=='y':
                local = input("Write local? (y/n):")
                if local.lower() == "y":
                    write_to_json(data)
                else:
                    fb.addData(data)
            break

if __name__ == '__main__':
    main()