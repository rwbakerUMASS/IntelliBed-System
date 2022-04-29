from firebase import Firebase
from firebase_config import CONFIG
import numpy as np
from matplotlib import pyplot as plt

fb = Firebase(CONFIG())
data = fb.getRawData()
keys = list(data.keys())
keyNum = []
for key in keys:
    keyNum.append(float(key.replace('-','.')))
diff = np.diff(keyNum)
plt.scatter(range(len(diff)),diff)
plt.show()