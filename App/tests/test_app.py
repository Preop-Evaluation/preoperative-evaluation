import os, tempfile, logging, unittest, pytest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import db
from App.controllers import *

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_patient(self):
        patient = Patient("bob", "bob", "bob", "bobpass", "bob@mail.com", "1234567")
        assert patient.username == "bob"

    def test_new_doctor(self):
        doctor = Doctor("jane", "doe", "JaneUser", "janepass", "jane@mail.com", "1234567")
        assert doctor.username == "JaneUser"

    def test_new_anestheiologist(self):
        anest = Anesthesiologist("jane", "doe", "JaneUser", "janepass", "jane@mail.pipcom", "1234567")
        assert anest.username == "JaneUser"

    def test_get_json(self):
        patient = Patient("1", "bob", "bob123", "bobpass", "bob@mail.com", "1234567")
        user_json = patient.get_json()
        self.assertEqual(user_json["username"], "bob123")

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        patient = Patient("bob", "bob", "bob", "bobpass", "bob@mail.com", "1234567")
        assert patient.password != password

    def test_check_password(self):
        password = "bobpass"
        patient = Patient("bob", "bob", "bob", "bobpass", "bob@mail.com", "1234567")
        assert patient.check_password(password)

    def test_password_not_in_json(self):
        patient = Patient("bob", "bob", "bob", "password", "bob@mail.com", "1234567")
        user_json = patient.get_json()
        self.assertNotIn("password", user_json)

    def test_invalid_login(self):
        patient = Patient("bob", "bob", "bob", "bobpass", "bob@mail.com", "1234567")
        self.assertFalse(patient.check_password("invalid"))


    #edge cases
    def test_patient_long_username(self):
        long_username = "bob" * 100
        patient = create_patient("bob", "bob", long_username, "bobpass", "bob@mail.com", "1274567")
        self.assertIsNone(patient) 

    def test_patient_long_firstname(self):
        long_name = "bob" * 100
        patient = create_patient(long_name, "bob", "bob", "bobpass", "bob@mail.com", "1274567")
        self.assertIsNone(patient)  
    
    def test_patient_long_lastname(self):
        long_name = "bob" * 100
        patient = create_patient("bob", long_name, "bob", "bobpass", "bob@mail.com", "1274567")
        self.assertIsNone(patient)  
    
    def test_patient_long_email(self):
        long_mail = "bob" * 100 + "@mail.com"
        patient = create_patient("bob", "bob", "bob", "bobpass", long_mail, "1274567")
        self.assertIsNone(patient)  


    def test_doctor_long_username(self):
        long_username = "bob" * 100
        doctor = create_doctor("bob", "bob", long_username, "bobpass", "bob@mail.com", "1274567")
        self.assertIsNone(doctor) 

    def test_doctor_long_firstname(self):
        long_name = "bob" * 100
        doctor = create_doctor(long_name, "bob", "bob", "bobpass", "bob@mail.com", "1274567")
        self.assertIsNone(doctor)  
    
    def test_doctor_long_lastname(self):
        long_name = "bob" * 100
        doctor = create_doctor("bob", long_name, "bob", "bobpass", "bob@mail.com", "1274567")
        self.assertIsNone(doctor)  
    
    def test_doctor_long_email(self):
        long_mail = "bob" * 100 + "@mail.com"
        doctor = create_doctor("bob", "bob", "bob", "bobpass", long_mail, "1274567")
        self.assertIsNone(doctor)  


    def test_anesth_long_username(self):
        long_username = "bob" * 100
        anesthesiologist = create_anesthesiologist("bob", "bob", long_username, "bobpass", "bob@mail.com", "1274567")
        self.assertIsNone(anesthesiologist) 

    def test_anesth_long_firstname(self):
        long_name = "bob" * 100
        anesthesiologist = create_anesthesiologist(long_name, "bob", "bob", "bobpass", "bob@mail.com", "1274567")
        self.assertIsNone(anesthesiologist)  
    
    def test_anesth_long_lastname(self):
        long_name = "bob" * 100
        anesthesiologist = create_anesthesiologist("bob", long_name, "bob", "bobpass", "bob@mail.com", "1274567")
        self.assertIsNone(anesthesiologist)  
    
    def test_anesth_long_email(self):
        long_mail = "bob" * 100 + "@mail.com"
        anesthesiologist = create_anesthesiologist("bob", "bob", "bob", "bobpass", long_mail, "1274567")
        self.assertIsNone(anesthesiologist)  
    







'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
# @pytest.fixture(autouse=True, scope="module")
# def empty_db():
#     app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
#     create_db()
#     yield app.test_client()
#     db.drop_all()


# def test_authenticate(self):
#     response = self.client.post('/signin', data={'email': 'bob@mail.com', 'password': 'bobpass'})
#     self.assertEqual(response.status_code, 302)


# class UsersIntegrationTests(unittest.TestCase):

#     def test_create_user(self):
#         user = create_user("rick", "bobpass")
#         assert user.username == "rick"

#     def test_get_all_users_json(self):
#         users_json = get_all_users_json()
#         self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

#     # Tests data changes in the database
#     def test_update_user(self):
#         update_user(1, "ronnie")
#         user = get_user(1)
#         assert user.username == "ronnie"
        
