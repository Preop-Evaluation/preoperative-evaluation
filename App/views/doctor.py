from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, current_app
from flask_login import current_user
from App.models import db, Questionnaire
from App.controllers import *
from App.models.patient import Patient
from App.models.anesthesiologist import Anesthesiologist
from flask_mail import Message
import pytz
from App.controllers.questions import get_all_flattened_questions
from App.controllers import doctor_required

doctor_views = Blueprint('doctor_views', __name__, template_folder='../templates')


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
    questions = get_all_flattened_questions()
    return render_template('questionnaire_view.html', questionnaire=questionnaire, questions=questions, title= 'Questionnaire')


@doctor_views.route('/dashboard/doctor/questionnaire/submit/<questionnaire_id>', methods=['POST'])
@doctor_required
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
        anesthesiologists = Anesthesiologist.query.all()

        flagged_str = ", ".join(questionnaire.doctor_flagged_questions) if questionnaire.doctor_flagged_questions else "None"

        if patient:
            ast_tz = pytz.timezone("America/Port_of_Spain")
            current_dt = questionnaire.submitted_date.astimezone(ast_tz).strftime("%d/%m/%Y - %I:%M %p") if questionnaire.submitted_date else ""

            msg = Message(
                subject="Your Questionnaire Needs Attention (Doctor Review)",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[patient.email]
            )
            msg.body = (
                f"Dear {patient.firstname},\n\n"
                f"Your questionnaire, Dated: {current_dt}, was declined by Dr. {current_user.firstname} {current_user.lastname}.\n"
                f"Flagged question(s): {flagged_str}\n"
                f"Doctor's Comments: {notes}\n\n"
                f"Please log in to update the flagged answers.\n\n"
                f"Regards,\nMedCareTT Team"
            )
            mail.send(msg)

            for anesth in anesthesiologists:
                msg_a = Message(
                    subject=f"Doctor flagged patient {patient.firstname}",
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[anesth.email]
                )
                msg_a.body = (
                    f"Dear Anesthesiologist {anesth.lastname},\n\n"
                    f"Dr. {current_user.firstname} {current_user.lastname} has declined the questionnaire (ID: {questionnaire.id}) "
                    f"for patient {patient.firstname} {patient.lastname}.\n"
                    f"Flagged question(s): {flagged_str}\n"
                    f"Doctor's Comments: {notes}\n\n"
                    f"Regards,\nMedCareTT Team"
                )
                mail.send(msg_a)

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
            msg.body = (
                f"Dear {patient.firstname},\n\n"
                f"Your questionnaire has been approved by Dr. {current_user.firstname} {current_user.lastname}.\n"
                f"Surgery is scheduled on {operation_date}.\n\n"
                f"Regards,\nDr. {current_user.lastname}"
            )
            mail.send(msg)

    flash("Review submitted successfully.")
    return redirect(url_for('doctor_views.doctor_questionnaire_page', questionnaire_id=questionnaire_id))


@doctor_views.route('/dashboard/doctor/toggle_flag', methods=['POST'])
@doctor_required
def doctor_toggle_flag():
    questionnaire_id = request.form.get('questionnaire_id')
    question_id = request.form.get('question_id')

    if not questionnaire_id or not question_id:
        return jsonify({'error': 'Missing parameters'}), 400

    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        return jsonify({'error': 'Questionnaire not found'}), 404

    flagged = set(questionnaire.doctor_flagged_questions or [])
    if question_id in flagged:
        flagged.remove(question_id)
        flag_state = False
    else:
        flagged.add(question_id)
        flag_state = True

    questionnaire.doctor_flagged_questions = list(flagged)
    db.session.commit()

    return jsonify({'flagged': flag_state})
