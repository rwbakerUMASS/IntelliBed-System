from hx711 import HX711
from firebase import Firebase
import time

config = {
  "apiKey": "AIzaSyBqmtDdXcCLp4ODEgtkelMj7QWEixxSVOY",
  "authDomain": "intelli--bed.firebaseapp.com",
  "databaseURL": "https://intelli--bed-default-rtdb.firebaseio.com/",
  "storageBucket": "intelli--bed.appspot.com"
}
prevTime = time.time()
data = {
  "mean":4,
  "stdev":34,
  "numPeaks":2
}
fb = Firebase(config)
# fb.clearTable()

hx = HX711(5,6)
hx.set_reading_format("MSB","MSB")
hx.set_reference_unit(1)
hx.reset()
hx.tare()
print(hx.get_weight())
hx.power_up()
hx.power_down()