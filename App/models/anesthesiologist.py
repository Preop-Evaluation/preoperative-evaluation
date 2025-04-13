from App.database import db
from .user import User
from .questionnaire import Questionnaire

class Anesthesiologist(User):
    __tablename__ = 'anesthesiologist'
    type = db.Column(db.String(120), nullable=False, default='anesthesiologist')

    def __init__(self, firstname, lastname, username, password, email, phone_number):
        super().__init__(firstname, lastname, username, password, email, phone_number)
        self.type = 'anesthesiologist'

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
    
    def update_questionnaire_anesthesiologist(self, questionnaire_id, new_anesthesiologist_notes, status):
        questionnaire = Questionnaire.query.get(questionnaire_id)
        if questionnaire:
            try:
                questionnaire.anesthesiologist_notes = new_anesthesiologist_notes
                questionnaire.status = status
                db.session.commit()
                return questionnaire
            except Exception as e:
                print(e, "Error updating anesthesiologist notes")
                return None         
        return None

    