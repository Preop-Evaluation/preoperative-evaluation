from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, current_app
from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db
from App.controllers import *
from App.models.questionnaire import Questionnaire
from App.database import db
from App.extensions import mail
from flask_mail import Message
from App.controllers import anesthesiologist_required
from App.models.patient import Patient
from App.controllers.questions import get_default_questionnaire
from App.controllers.questionnaire import get_questionnaire
import json
import pytz
from App.controllers.questions import get_all_flattened_questions

anesthesiologist_views = Blueprint('anesthesiologist_views', __name__, template_folder='../templates')


'''
Page Routes
'''

@anesthesiologist_views.route('/dashboard/anesthesiologist', methods=['GET'])
@anesthesiologist_required
def anesthesiologist_dashboard_page():
    patients = get_all_patients()
    patient_questionnaires = get_all_questionnaires()
    return render_template('anesthesiologist_dashboard.html', patient_questionnaires=patient_questionnaires, patients=patients, title= 'Anesthesiologist Dashboard')


@anesthesiologist_views.route('/dashboard/anesthesiologist/patient/<patient_id>', methods=['GET'])
@anesthesiologist_required
def anesthesiologist_patient_info_page(patient_id):
    patient = get_patient_by_id(patient_id)
    return render_template('patient_info.html', patient=patient, title= 'Patient Information')

@anesthesiologist_views.route('/dashboard/anesthesiologist/questionnaire/<questionnaire_id>', methods=['GET'])
@anesthesiologist_required
def anesthesiologist_questionnaire_page(questionnaire_id):
    questionnaire = get_questionnaire(questionnaire_id)
    questions = get_all_flattened_questions()
    return render_template('questionnaire_view.html', questionnaire=questionnaire, questions=questions, title="Questionnaire Review")

'''
Action Routes
'''

@anesthesiologist_views.route('/dashboard/anesthesiologist/questionnaire/submit/<questionnaire_id>', methods=['POST'])
@anesthesiologist_required
def update_questionnaire_anesthesiologist_action(questionnaire_id):
    data = request.form    
    status = data.get('status')
    notes = data.get('anesthesiologist_notes')
    
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        flash("Questionnaire not found.")
        return redirect(url_for('anesthesiologist_views.anesthesiologist_questionnaire_page', questionnaire_id=questionnaire_id))
    
    if status.lower() == "declined":
        if not questionnaire.previous_responses:
            questionnaire.previous_responses = questionnaire.responses.copy() if questionnaire.responses else {}
        questionnaire.status = "declined"
        questionnaire.anesthesiologist_notes = notes
        db.session.commit()
        patient = Patient.query.get(questionnaire.patient_id)
        if patient:
            ast_tz = pytz.timezone("America/Port_of_Spain")
            if questionnaire.submitted_date:
                submitted_dt_ast = questionnaire.submitted_date.astimezone(ast_tz)
                current_dt = submitted_dt_ast.strftime("%d/%m/%Y - %I:%M %p")
            else:
                current_dt = ""
            flagged_str = ", ".join(questionnaire.flagged_questions) if questionnaire.flagged_questions else "None"
            msg = Message(
                subject="Your Questionnaire Needs Attention",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[patient.email]
            )
            msg.body = (f"Dear {patient.firstname},\n\n"
                        f"Your submitted questionnaire, Dated: {current_dt} has been declined.\n"
                        f"Flagged question(s): {flagged_str}\n"
                        f"Review Comments: {notes}\n\n"
                        f"Please log in to update the flagged answers.\n\n"
                        f"Regards,\nMedCareTT Team")
            try:
                mail.send(msg)
            except Exception as e:
                print("Error sending decline email:", e)
    else:
        questionnaire.status = status
        questionnaire.anesthesiologist_notes = notes
        db.session.commit()
    flash("Review submitted successfully.")
    return redirect(url_for('anesthesiologist_views.anesthesiologist_questionnaire_page', questionnaire_id=questionnaire_id))


@anesthesiologist_views.route('/dashboard/anesthesiologist/toggle_flag', methods=['POST'])
@anesthesiologist_required
def toggle_flag():
    questionnaire_id = request.form.get('questionnaire_id')
    question_id = request.form.get('question_id')
    if not questionnaire_id or not question_id:
        return jsonify({'error': 'Missing parameters'}), 400

    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        return jsonify({'error': 'Questionnaire not found'}), 404

    flagged = set(questionnaire.flagged_questions) if questionnaire.flagged_questions else set()
    if question_id in flagged:
        flagged.remove(question_id)
        flag_state = False
    else:
        flagged.add(question_id)
        flag_state = True

    questionnaire.flagged_questions = list(flagged)
    db.session.commit()
    return jsonify({'flagged': flag_state})
