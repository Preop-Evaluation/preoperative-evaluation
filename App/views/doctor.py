from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db, Questionnaire
from App.controllers import *
from datetime import datetime
from App.models.patient import Patient
import pytz
from App.controllers import doctor_required
from flask_mail import Message

doctor_views = Blueprint('doctor_views', __name__, template_folder='../templates')

'''
Page Routes
'''


@doctor_views.route('/dashboard/doctor', methods=['GET'])
@doctor_required
def doctor_dashboard_page():
    patients = get_all_patients()
    patient_questionnaires = get_all_questionnaires()
    return render_template('doctor_dashboard.html', patient_questionnaires=patient_questionnaires, patients=patients, title= 'Doctor Dashboard')

@doctor_views.route('/dashboard/doctor/patient/<patient_id>', methods=['GET'])
@doctor_required
def doctor_patient_info_page(patient_id):
    patient = get_patient_by_id(patient_id)
    return render_template('patient_info.html', patient=patient, title= 'Patient Infomation')

@doctor_views.route('/dashboard/doctor/questionnaire', methods=['GET'])
@doctor_required
def doctor_questionnaire_page():
    questionnaire_id = request.args.get('questionnaire_id')
    questionnaire = get_questionnaire(questionnaire_id)
    questions = get_default_questionnaire()
    return render_template('questionnaire_view.html', questionnaire=questionnaire, questions=questions, title= 'Questionnaire')


'''
Action Routes
'''

@doctor_views.route('/dashboard/doctor/questionnaire/submit/<questionnaire_id>', methods=['POST'])
def update_questionnaire_doctor_action(questionnaire_id):
    data = request.form     
    operation_date = data.get('operation_date')
    notes = data.get('doctor_notes')
    
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        flash("Questionnaire not found.")
        return redirect(url_for('doctor_views.doctor_questionnaire_page', questionnaire_id=questionnaire_id))
    
    if data.get('status', '').lower() == "declined":
        if not questionnaire.previous_responses:
            questionnaire.previous_responses = questionnaire.responses.copy() if questionnaire.responses else {}
        questionnaire.status = "declined"
        questionnaire.doctor_notes = notes
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
                subject="Your Questionnaire Needs Attention (Doctor Review)",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[patient.email]
            )
            msg.body = (f"Dear {patient.firstname},\n\n"
                        f"Your submitted questionnaire, Dated: {current_dt} has been declined by Dr. {current_user.firstname} {current_user.lastname}.\n"
                        f"Flagged question(s): {flagged_str}\n"
                        f"Doctor's Comments: {notes}\n"
                        f"Anesthesiologist's Comments: {questionnaire.anesthesiologist_notes or 'N/A'}\n\n"
                        f"Please log in to update the flagged answers accordingly.\n\n"
                        f"Regards,\nMedCareTT Team")
            try:
                mail.send(msg)
            except Exception as e:
                print("Error sending decline email on doctor side:", e)
    else:
        questionnaire.status = "approved"
        questionnaire.doctor_notes = notes
        questionnaire.operation_date = operation_date
        db.session.commit()
        patient = Patient.query.get(questionnaire.patient_id)
        if patient:
            msg = Message(
                subject="Surgery Scheduled",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[patient.email]
            )
            try:
                ast_tz = pytz.timezone("America/Port_of_Spain")
                if questionnaire.submitted_date:
                    submitted_dt_ast = questionnaire.submitted_date.astimezone(ast_tz)
                    formatted_date = submitted_dt_ast.strftime("%d/%m/%Y - %I:%M %p")
                else:
                    formatted_date = "Unknown"

                msg.body = (
                            f"Dear {patient.firstname},\n\n"
                            f"Your questionnaire has been approved by Dr. {current_user.firstname} {current_user.lastname}.\n"
                            f"Surgery is scheduled on {operation_date}.\n"
                            f"Regards,\nDr. {current_user.lastname}"
                        )
            except Exception as e:
                print("Error formatting email date:", e)
            try:
                mail.send(msg)
            except Exception as e:
                print("Error sending approval email on doctor side:", e)
    
    flash("Review submitted successfully.")
    return redirect(url_for('doctor_views.doctor_questionnaire_page', questionnaire_id=questionnaire_id))