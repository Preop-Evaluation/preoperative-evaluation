from App.models import Questionnaire
from App.database import db
from App.controllers.patient import set_patient_autofill_enabled

def create_questionnaire(patient_id, responses):
    try:
        new_questionnaire = Questionnaire(patient_id=patient_id, responses=responses)
        db.session.add(new_questionnaire)
        db.session.commit()
        set_patient_autofill_enabled(patient_id, True)
        return new_questionnaire
    except Exception as e:
        print(e, "Error creating questionnaire")
        return None
    
def get_questionnaire(id):
    return Questionnaire.query.get(id)

def get_all_questionnaires():
    return Questionnaire.query.all()

def get_all_questionnaires_json():
    questionnaires = Questionnaire.query.all()
    if not questionnaires:
        return []
    questionnaires = [questionnaire.get_json() for questionnaire in questionnaires]
    return questionnaires

def get_questionnaire_by_patient_id(patient_id):
    return Questionnaire.query.filter_by(patient_id=patient_id).first()

def get_questionnaire_by_status(status):
    return Questionnaire.query.filter_by(status=status).all()

def get_questionnaire_by_status_json(status):
    questionnaires = Questionnaire.query.filter_by(status=status).all()
    if not questionnaires:
        return []
    questionnaires = [questionnaire.get_json() for questionnaire in questionnaires]
    return questionnaires

def get_latest_questionnaire(patient_id):
    return Questionnaire.query.filter_by(patient_id=patient_id).order_by(Questionnaire.submitted_date.desc()).first()

    
    