from sklearn.metrics import confusion_matrix, f1_score
from firebase import Firebase
from firebase_config import CONFIG
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import json
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.model_selection import KFold

fb = Firebase(CONFIG())
# data = fb.getRawData()
with open('data.json', 'r+') as f:
    data = json.load(f)
    data = data['data']
keys = list(data.keys())
timestamp = []
x=[]
y=[]
classification = []
for key in keys:
    timestamp.append(float(key.replace('-','.')))
    x.append(data[key]['data']['X'])
    y.append(data[key]['data']['Y'])
    classification.append(data[key]['class'])

x=np.array(x)
y=np.array(y)
timestamp=np.array(timestamp)

features = []

plt.figure(1)
plt.subplot(3,1,1)
plt.yticks([0,1,2,3],['Stationary','Rolling','Sitting Up','Slight Adjust'])
plt.plot(range(len(classification)),classification)
plt.subplot(3,1,2)
plt.ylabel('X Position')
plt.plot(range(len(x)),x)
plt.subplot(3,1,3)
plt.ylabel('Y Position')
plt.plot(range(len(y)),y)

windowSize = 32
windowStep = 4
numWindows = int((len(x)-windowSize)/windowStep)+1
for i in range(numWindows):

    windowStart = i*windowStep
    windowEnd = i*windowStep+windowSize

    xSlice = x[windowStart:windowEnd]
    ySlice = y[windowStart:windowEnd]
    cSlice = classification[windowStart:windowEnd]

    meanX = np.mean(xSlice)
    meanY = np.mean(ySlice)
    medianX = np.median(xSlice)
    medianY = np.median(ySlice)
    stdX = np.std(xSlice)
    stdY = np.std(ySlice)
    varX = np.var(xSlice)
    varY = np.var(ySlice)
    slopeX = np.polyfit(range(len(xSlice)),xSlice,1)[0]
    slopeY = np.polyfit(range(len(ySlice)),ySlice,1)[0]
    rmsX = np.sqrt(np.mean(xSlice**2))
    rmsY = np.sqrt(np.mean(ySlice**2))

    c,_ = stats.mode(cSlice)
    c = int(c[0])

    features.append([c,meanX,meanY,medianX,medianY,stdX,stdY,varX,varY,slopeX,slopeY,rmsX,rmsY])

features = np.array(features,dtype=np.float16)

i=1

plt.figure(2)
plt.subplot(3,1,1)
plt.yticks([0,1,2,3],['Stationary','Rolling','Sitting Up','Slight Adjust'])
plt.plot(range(numWindows),features[:,0])
plt.subplot(3,1,2)
plt.ylabel('X Position')
plt.plot(range(numWindows),features[:,i])
plt.subplot(3,1,3)
plt.ylabel('Y Position')
plt.plot(range(numWindows),features[:,i+1])

plt.show()

X = features[:,1:]
y = features[:,0]

kf = KFold(n_splits=5, shuffle=True)
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    model = knn(n_neighbors=10)
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    print(f1_score(y_test,y_pred,average='macro'))
    print(confusion_matrix(y_test,y_pred))