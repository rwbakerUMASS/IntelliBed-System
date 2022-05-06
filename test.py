from sqlite3 import Timestamp
from scipy import rand
from hx711 import HX711
from firebase import Firebase
import time
from firebase_config import CONFIG
import json
from data_gathering import write_to_json
import random
import numpy as np

data={}
classification = 0
for i in range(1000):
  timestamp=time.time()
  time.sleep(0.05)
  if random.randint(0,50) == 0:
    classification=random.randint(0,10)
  vals = [1,1,1,1]
  x=random.random()+i
  y=random.random()+np.sin(i)
  data[timestamp]={"class":classification,"data":{"sensor":vals,"X":x,"Y":y}}

write_to_json(data)


# prevTime = time.time()
# features = {
#   "mean":4,
#   "stdev":34,
#   "numPeaks":2,
#   "timestamps":[prevTime]
# }
# data = {
#   "sensor":[100,333,445,343],
#   "x":0.5,
#   "y":0.3
# }
# classification=1
# fb = Firebase(CONFIG())
# fb.clearTable()
# fb.addFeatures(1,features,classification)
# fb.addData(prevTime,data)
