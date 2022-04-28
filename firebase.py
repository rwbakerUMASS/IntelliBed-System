from os import times
import pyrebase

class Firebase:

  def __init__(self, config):
    self.firebase = pyrebase.initialize_app(config)
    self.db = self.firebase.database()

  def clearTable(self):
    for key in self.db.get().val():
      self.db.child(key).remove()

  def addFeatures(self, index, data, classification=None):
    self.db.child("window").child(index).child('features').set(data) 
    self.db.child("window").child(index).child('class').set(classification)
  
  def addData(self, timestamp, data, classification=None):
    timestamp=str(timestamp).replace(".","-")
    self.db.child("data").child(timestamp).child("data").set(data)
    self.db.child("data").child(timestamp).child("class").set(classification)
    

