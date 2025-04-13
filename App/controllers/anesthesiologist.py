from App.models import Anesthesiologist
from App.models import db
from App.controllers.notification import create_notification

def create_anesthesiologist(firstname, lastname, username, password, email, phone_number):
    try:
        new_anesthesiologist = Anesthesiologist(firstname=firstname, lastname=lastname, username=username, password=password, email=email, phone_number=phone_number)
        db.session.add(new_anesthesiologist)
        db.session.commit()
        return new_anesthesiologist
    except Exception as e:
        print(e, "Error creating anesthesiologist")
        return None


def update_questionnaire_anesthesiologist(anesthesiologist_id, questionnaire_id, new_anesthesiologist_notes, status):
    anesthesiologist = Anesthesiologist.query.get(anesthesiologist_id)
    if anesthesiologist:        
        questionnaire = anesthesiologist.update_questionnaire_anesthesiologist(questionnaire_id, new_anesthesiologist_notes, status)
        if questionnaire:
            notification = create_notification(questionnaire.patient_id, f"Anesthesiologist {anesthesiologist.lastname} has reviewed your questionnaire", "Questionnaire Updated")
            return True
        else:
            return False
    else:
        return False  


def delete_anesthesiologist(username):
    try:
        anesthesiologist = Anesthesiologist.query.filter_by(username=username).first()
        if not anesthesiologist:
            print(f"Anesthesiologist with username '{username}' not found.")
            return False

        db.session.delete(anesthesiologist)
        db.session.commit()
        print(f"Anesthesiologist {anesthesiologist.firstname} {anesthesiologist.lastname} deleted successfully.")
        return True
    except Exception as e:
        print(e, "Error deleting anesthesiologist")
        return False


def update_anesthesiologist(username, firstname=None, lastname=None, new_username=None, password=None, email=None, phone_number=None):
    try:
        anesthesiologist = Anesthesiologist.query.filter_by(username=username).first()
        if not anesthesiologist:
            print(f"Anesthesiologist with username '{username}' not found.")
            return None

        if firstname:
            anesthesiologist.firstname = firstname
        if lastname:
            anesthesiologist.lastname = lastname
        if new_username:
            anesthesiologist.username = new_username
        if password:
            anesthesiologist.set_password(password)  
        if email:
            anesthesiologist.email = email
        if phone_number:
            anesthesiologist.phone_number = phone_number

        db.session.commit()
        print(f"Anesthesiologist {anesthesiologist.firstname} {anesthesiologist.lastname} updated successfully.")
        return anesthesiologist
    except Exception as e:
        print(e, "Error updating anesthesiologist")
        return None
        

def get_all_anesthesiologists():
    anesthesiologists = Anesthesiologist.query.all()
    return [
        {
            "id": anesthesiologist.id,
            "name": f"{anesthesiologist.firstname} {anesthesiologist.lastname}",
            "username": anesthesiologist.username,
            "email": anesthesiologist.email,
            "role": "Anesthesiologist"
        }
        for anesthesiologist in anesthesiologists
    ]
