from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
import uuid

def generate_short_uuid():
        return str(uuid.uuid4())[:8]
class User(db.Model, UserMixin):
    __abstract__ = True
    __tablename__ = 'user'
    id = db.Column(db.String(20), primary_key=True, default=generate_short_uuid, server_default='gen_random_uuid()') 
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    username =  db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(1200), nullable=False)
    email = db.Column(db.String(150), nullable = False, unique = True)
    phone_number = db.Column(db.String(60), nullable = False, unique = True)
 
    def __init__(self, firstname, lastname, username, password, email, phone_number):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.set_password(password)
        self.email = email
        self.phone_number = phone_number

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    

    
