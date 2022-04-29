from os import times
import pyrebase

class Firebase:

  def __init__(self, config):
    self.firebase = pyrebase.initialize_app(config)
    self.db = self.firebase.database()

  def clearTable(self):
    if self.db.get().val() is None:
      return
    for key in self.db.get().val():
      self.db.child(key).remove()

  def getRawData(self):
    return self.db.child('data').get().val()

  def addFeatures(self, index, data, classification=None):
    self.db.child("window").child(index).child('features').set(data) 
    self.db.child("window").child(index).child('class').set(classification)
  
  def addData(self,data):
    for key in data:
      self.db.child("data").child("key").set(data[key])
    
if __name__ == "__main__":
  print("FB")
  fb = Firebase(config = {
    "apiKey": "AIzaSyBqmtDdXcCLp4ODEgtkelMj7QWEixxSVOY",
    "authDomain": "intelli--bed.firebaseapp.com",
    "databaseURL": "https://intelli--bed-default-rtdb.firebaseio.com/",
    "storageBucket": "intelli--bed.appspot.com"
  })