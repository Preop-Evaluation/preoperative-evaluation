from App.models import Doctor
from App.database import db
from App.controllers.notification import create_notification
from flask import current_app
from App.extensions import mail
from flask_mail import Message
from App.models.patient import Patient
import pytz

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
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        questionnaire = doctor.update_questionnaire_doctor(questionnaire_id, new_doctor_notes, new_operation_date)
        if questionnaire:
            notification = create_notification(
                questionnaire.patient_id, 
                f"Doctor {doctor.lastname} has reviewed your questionnaire",
                "Questionnaire Updated"
            )
            patient = Patient.query.get(questionnaire.patient_id)
            if patient:
                msg = Message(
                    subject="Surgery Date Scheduled",
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[patient.email]
                )
                msg.body = (
                    f"Dear {patient.firstname},\n\n"
                    f"Your surgery is scheduled on {new_operation_date}.\n\n"
                    f"Regards,\nDr. {doctor.lastname}"
                )
                mail.send(msg)
            return True
        else:
            return False
    else:
        return False


def delete_doctor(username):
    try:
        doctor = Doctor.query.filter_by(username=username).first()
        if not doctor:
            print(f"Doctor with username '{username}' not found.")
            return False

        db.session.delete(doctor)
        db.session.commit()
        print(f"Doctor {doctor.firstname} {doctor.lastname} deleted successfully.")
        return True
    except Exception as e:
        print(e, "Error deleting doctor")
        return False


def update_doctor(username, firstname=None, lastname=None, new_username=None, password=None, email=None, phone_number=None):
    try:
        doctor = Doctor.query.filter_by(username=username).first()
        if not doctor:
            print(f"Doctor with username '{username}' not found.")
            return None

        if firstname:
            doctor.firstname = firstname
        if lastname:
            doctor.lastname = lastname
        if new_username:
            doctor.username = new_username
        if password:
            doctor.set_password(password)
        if email:
            doctor.email = email
        if phone_number:
            doctor.phone_number = phone_number

        db.session.commit()
        print(f"Doctor {doctor.firstname} {doctor.lastname} updated successfully.")
        return doctor
    except Exception as e:
        print(e, "Error updating doctor")
        return None

def get_all_doctors():
    doctors = Doctor.query.all()
    return [
        {
            "id": doctor.id,
            "name": f"{doctor.firstname} {doctor.lastname}",
            "username": doctor.username,
            "email": doctor.email,
            "role": "Doctor"
        }
        for doctor in doctors
    ]


