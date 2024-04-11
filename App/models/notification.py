from datetime import datetime
from App.database import db

class Notification(db.Model):
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(220), db.ForeignKey('patient.id'))
    title = db.Column(db.String(220))
    message = db.Column(db.String(220))
    timestamp=db.Column(db.DateTime,default = datetime.now())
    seen = db.Column(db.Boolean, default=False)
    
    def __init__(self, patient_id, message, title):
        self.patient_id = patient_id
        self.message = message
        self.title = title
        self.timestamp = datetime.now()
        
    
    def toDict(self):
        return{
            'id':self.id,
            'patient_id': self.patient_id,
            'message': self.message,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_json(self):
        return{
            'id':self.id,
            'patient_id': self.patient_id,
            'message': self.message,
            'title': self.title,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }