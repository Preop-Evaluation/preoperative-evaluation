from App.models import Doctor
from App.database import db
from App.controllers.notification import create_notification

def create_doctor(firstname, lastname, username, password, email, phone_number):
    try:
        new_doctor = Doctor(firstname=firstname, lastname=lastname, username=username, password=password, email=email, phone_number=phone_number)
        db.session.add(new_doctor)
        db.session.commit()
        return new_doctor
    except Exception as e:
        print(e, "Error creating doctor")
        return None
    

def update_questionnaire_doctor(doctor_id, questionnaire_id, new_doctor_notes, new_operation_date):
    # Verify the doctor's existence and authority
    doctor = Doctor.query.get(doctor_id)
    if doctor:        
        questionnaire = doctor.update_questionnaire_doctor(questionnaire_id, new_doctor_notes, new_operation_date)
        if questionnaire:
            notification = create_notification(questionnaire.patient_id, f"Doctor {doctor.lastname} has updated your questionnaire", "Questionnaire Updated")
            return True
        else:
            return False
    else:
        return False  # Doctor not found or not authorized