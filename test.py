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
features = {
  "mean":4,
  "stdev":34,
  "numPeaks":2,
  "timestamps":[prevTime]
}
data = {
  "sensor":[100,333,445,343],
  "x":0.5,
  "y":0.3
}
classification=1
fb = Firebase(config)
fb.clearTable()
fb.addFeatures(1,features,classification)
fb.addData(prevTime,data)
