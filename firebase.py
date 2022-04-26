import pyrebase

class Firebase:

  def __init__(self, config):
    self.firebase = pyrebase.initialize_app(config)
    self.db = self.firebase.database()

  def clearTable(self):
    for key in self.db.get().val():
      self.db.child(key).remove()

  def addData(self, timestamp, data):
    self.db.child("data").child(timestamp).set(data)
  
  def setBedWeight(self,weight):
    self.db.child("bed_weight").set(weight)
  
  def setUserWeight(self,weight):
    self.db.child("user_weight").set(weight)