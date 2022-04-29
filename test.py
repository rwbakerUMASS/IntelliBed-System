from hx711 import HX711
from firebase import Firebase
import time
from firebase_config import CONFIG
import json




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
