from App.database import db
from .user import User
from .questionnaire import Questionnaire

class Doctor(User):    
    __tablename__ = 'doctor'
    type = db.Column(db.String(120), nullable=False, default='doctor')

    def __init__(self, firstname, lastname, username, password, email, phone_number):
        super().__init__(firstname, lastname, username, password, email, phone_number)
        self.type = 'doctor'

    def get_json(self):
        return{
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'type': self.type
        }
    
    def update_questionnaire_doctor(self, questionnaire_id, new_doctor_notes, new_operation_date):
        questionnaire = Questionnaire.query.get(questionnaire_id)
        if questionnaire:
            try:
                questionnaire.doctor_notes = new_doctor_notes
                questionnaire.operation_date = new_operation_date
                db.session.commit()
                return questionnaire
            except Exception as e:
                print(e, "Error updating doctor notes")
                return None        
        return None

