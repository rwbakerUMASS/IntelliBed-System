from hx711 import HX711
from firebase import Firebase
import RPi.GPIO as GPIO
from hx711 import HX711
import time
import numpy as np

def findBase(sensor,num_samples):
    vals=[]
    print("Finding Base Scalar...")
    hx.set_reference_unit(1)
    for i in range(num_samples):
        vals.append(hx.get_weight(5))
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        print(vals[i])
    mean=np.mean(vals)
    print("Base = ",mean)
    return mean


def calibrateSensors(sensors):
    base = findBase(sensors[0],10)
    baseline = sensors[0].get_weight(5)
    sensors[0].set_reference_unit(base)
    sensors[1].set_reference_unit(base*baseline/sensors[1].get_weight(5))
    sensors[2].set_reference_unit(base*baseline/sensors[2].get_weight(5))
    sensors[3].set_reference_unit(base*baseline/sensors[3].get_weight(5))

config = {
  "apiKey": "AIzaSyBqmtDdXcCLp4ODEgtkelMj7QWEixxSVOY",
  "authDomain": "intelli--bed.firebaseapp.com",
  "databaseURL": "https://intelli--bed-default-rtdb.firebaseio.com/",
  "storageBucket": "intelli--bed.appspot.com"
}

sensors = [HX711(20,21),HX711(12,16),HX711(17,27),HX711(5,6)]
print("Setting HX711 Reading Format...")
for hx in sensors:
    hx.set_reading_format("MSB", "MSB") 
    hx.tare()
calibrateSensors(sensors)
for hx in sensors:
    hx.reset()
    hx.tare()

fb = Firebase(config)

classification = input("Input activity")


while True:
    timestamp = time.time()
    vals = []
    for hx in sensors:
        vals.append(hx.get_weight(1))
        hx.power_down()
        hx.power_up()
    data={"sensor":vals}
    # fb.addData(timestamp,data)
    print(data)
    time.sleep(0.1)

