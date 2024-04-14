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
    # Verify the anesthesiologist's existence and authority
    anesthesiologist = Anesthesiologist.query.get(anesthesiologist_id)
    if anesthesiologist:        
        questionnaire = anesthesiologist.update_questionnaire_anesthesiologist(questionnaire_id, new_anesthesiologist_notes, status)
        if questionnaire:
            notification = create_notification(questionnaire.patient_id, f"Anesthesiologist {anesthesiologist.lastname} has reviewed your questionnaire", "Questionnaire Updated")
            return True
        else:
            return False
    else:
        return False  # Anesthesiologist not found or not authorized
