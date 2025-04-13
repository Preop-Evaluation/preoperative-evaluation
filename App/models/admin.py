from App.database import db
from App.models.user import User

class Admin(User):
    __tablename__ = 'admin'
    type = db.Column(db.String(120), nullable=False, default='admin')

    def __init__(self, firstname, lastname, username, password, email, phone_number):
        super().__init__(firstname, lastname, username, password, email, phone_number)
        self.type = 'admin'

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone_number': self.phone_number,
            'type': self.type
        }
