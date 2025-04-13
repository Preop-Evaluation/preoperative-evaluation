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
    
def create_medical_history(patient_id, age, blood_type, weight, height, allergies, medical_conditions, medication):
    patient = Patient.query.get(patient_id)

    if not patient:
        print("Error: Patient not found.")
        return None

    # age = int(age) 
    # if age < 0 or age > 120:
    #     print("Error: Invalid age " + str(age) + ". Age must be between 0 and 120.")
    #     return None
    
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
    
def get_medical_history(patient_id):
    patient = Patient.query.get(patient_id)

    if not patient:
        print("Error: Patient not found.")
        return None

    try:
        return {
            'age': patient.age,
            'blood_type': patient.blood_type,
            'weight': patient.weight,
            'height': patient.height,
            'allergies': patient.allergies,
            'medical_conditions': patient.medical_conditions,
            'medication': patient.medication
        }
    except Exception as e:
        print(e, "Error retrieving medical history")
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

def delete_patient(username):
    try:
        patient = Patient.query.filter_by(username=username).first()
        if not patient:
            print(f"Patient with username '{username}' not found.")
            return False
        db.session.delete(patient)
        db.session.commit()
        print(f"Patient {patient.firstname} {patient.lastname} deleted successfully.")
        return True
    except Exception as e:
        print(e, "Error deleting patient")
        return False
