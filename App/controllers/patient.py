from App.database import db
from App.models import Patient

def create_patient(firstname, lastname, username, password, email, phone_number):
    try:
        new_patient = Patient(firstname=firstname, lastname=lastname, username=username, password=password, email=email, phone_number=phone_number)
        db.session.add(new_patient)
        db.session.commit()
        return new_patient
    except Exception as e:
        print(e, "Error creating patient")
        return None
    
def create_medical_history(patient_id,age, blood_type, weight, height, allergies, medical_conditions, medication):
    patient = Patient.query.get(patient_id)
    try:
        patient.age = age
        patient.blood_type = blood_type
        patient.weight = weight
        patient.height = height
        patient.allergies = allergies
        patient.medical_conditions = medical_conditions
        patient.medication = medication
        patient.med_history_updated = True        
        db.session.commit()
        return patient
    except Exception as e:
        print(e, "Error creating medical history")
        return None
    
def get_all_patients():
    return Patient.query.all()

def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)

def set_patient_autofill_enabled(patient_id, status):
    patient = Patient.query.get(patient_id)
    if patient.autofill_enabled == status:
        return True
    try:
        patient.autofill_enabled = status
        db.session.commit()
        return True
    except Exception as e:
        print(e, "Error setting autofill status")
        return False


def update_patient(username, firstname=None, lastname=None, new_username=None, password=None, email=None, phone_number=None):
    try:
        patient = Patient.query.filter_by(username=username).first()
        
        if not patient:
            return None  
        
        if firstname:
            patient.firstname = firstname
        if lastname:
            patient.lastname = lastname
        if new_username:
            patient.username = new_username
        if password:
            patient.password = password
        if email:
            patient.email = email
        if phone_number:
            patient.phone_number = phone_number
        
        db.session.commit()
        print(f"Patient {patient.firstname} {patient.lastname} updated successfully.")
        return patient
    
    except Exception as e:
        print(f"Error updating patient: {e}")
