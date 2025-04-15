from flask import Blueprint, redirect, render_template, request, jsonify, url_for, flash, current_app
from flask_login import current_user
import pytz
from App.models import db
from App.controllers import *
from App.controllers.questionnaire import get_questionnaire, create_questionnaire, get_latest_questionnaire
from App.controllers.questions import get_default_questionnaire
from App.models.anesthesiologist import Anesthesiologist
from flask_mail import Message
from App.extensions import mail

questionnaire_views = Blueprint('questionnaire_views', __name__, template_folder='../templates')

@questionnaire_views.route('/questionnaire', methods=['GET', 'POST'])
@patient_required
def questionnaire_page():
    questions = get_default_questionnaire()
    if current_user.med_history_updated:
        latest_responses = None
        if current_user.autofill_enabled:
            latest = get_latest_questionnaire(current_user.id)
            if latest:
                latest_responses = latest.responses
        return render_template('questionnaire_form.html', questions=questions, latest_responses=latest_responses, title="Questionnaire")
    else:
        return redirect(url_for('patient_views.patient_profile_page'))

@questionnaire_views.route('/questionnaire/details', methods=['GET', 'POST'])
@patient_required
def questionnaire_details_page():
    questionnaire_id = request.args.get('questionnaire_id')
    questionnaire = get_questionnaire(questionnaire_id)
    if not questionnaire:
        flash('Invalid questionnaire ID')
        return redirect(url_for('questionnaire_views.questionnaire_page'))

    questions = get_default_questionnaire()
    formatted_date = ""
    if questionnaire.submitted_date:
        ast_tz = pytz.timezone("America/Port_of_Spain")
        formatted_date = questionnaire.submitted_date.astimezone(ast_tz).strftime("%d/%m/%Y - %I:%M %p")

    return render_template('questionnaire_view.html', questions=questions, questionnaire=questionnaire, formatted_date=formatted_date, title="Questionnaire Details")

@questionnaire_views.route('/submit_questionnaire', methods=['POST'])
@patient_required
def submit_questionnaire():
    questions = get_default_questionnaire()
    responses = {}
    for key, value in request.form.items():
        if key.startswith('question_'):
            question_id = key.split('_')[1]
            responses[question_id] = value
    for question in questions:
        if question.get('follow_ups'):
            for follow_up in question['follow_ups']:
                follow_up_id = 'question_' + follow_up['id']
                if follow_up_id in request.form:
                    responses[follow_up['id']] = request.form[follow_up_id]
    questionnaire = create_questionnaire(patient_id=current_user.id, responses=responses)
    if questionnaire:
        flash('Questionnaire submitted successfully!')
    else:
        flash('Error submitting questionnaire!')
    return render_template('questionnaire_view.html', questions=questions, questionnaire=questionnaire, title="Questionnaire Details")

@questionnaire_views.route('/update_flagged_questionnaire/<questionnaire_id>', methods=['GET', 'POST'])
@patient_required
def update_flagged_questionnaire(questionnaire_id):
    questionnaire = get_questionnaire(questionnaire_id)
    if not questionnaire:
        flash("Questionnaire not found.")
        return redirect(url_for("questionnaire_views.questionnaire_page"))
    flagged_ids = (questionnaire.flagged_questions or []) + (questionnaire.doctor_flagged_questions or [])
    if questionnaire.status.lower() != "declined" or not flagged_ids:
        flash("No flagged questions to update.")
        return redirect(url_for("patient_views.patient_profile_page"))
    questions = get_default_questionnaire()
    flagged_questions = [q for q in questions if q["id"] in flagged_ids]
    if request.method == "POST":
        new_answers = {}
        for question in flagged_questions:
            qid = question["id"]
            answer = request.form.get("question_" + qid)
            if answer is not None:
                new_answers[qid] = answer
            if question.get("follow_ups"):
                for follow_up in question["follow_ups"]:
                    fid = follow_up["id"]
                    follow_up_answer = request.form.get("question_" + fid)
                    if follow_up_answer is not None:
                        new_answers[fid] = follow_up_answer
        if not questionnaire.previous_responses:
            questionnaire.previous_responses = {}
        if not questionnaire.anesthesiologist_updates:
            questionnaire.anesthesiologist_updates = {}
        if not questionnaire.doctor_updates:
            questionnaire.doctor_updates = {}
        for qid, answer in new_answers.items():
            questionnaire.previous_responses[qid] = questionnaire.responses.get(qid)
            if qid in (questionnaire.flagged_questions or []):
                questionnaire.anesthesiologist_updates[qid] = answer
            if qid in (questionnaire.doctor_flagged_questions or []):
                questionnaire.doctor_updates[qid] = answer
            questionnaire.responses[qid] = answer
        questionnaire.flagged_questions = []
        questionnaire.doctor_flagged_questions = []
        questionnaire.status = "pending"
        db.session.commit()
        anesthesiologists = Anesthesiologist.query.all()
        for anesth in anesthesiologists:
            msg = Message(
                subject=f"Patient {current_user.firstname} Updated Flagged Answers",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[anesth.email]
            )
            msg.body = (
                f"Dear Anesthesiologist {anesth.lastname},\n\n"
                f"Patient {current_user.firstname} {current_user.lastname} has updated the flagged answers on their questionnaire (ID: {questionnaire.id}).\n"
                f"Please log in to review the changes.\n\n"
                f"Regards,\nMedCareTT Team"
            )
            try:
                mail.send(msg)
            except Exception as e:
                print("Error sending update email to anesthesiologist:", e)

        flash("Your flagged questions have been updated. Your questionnaire is now pending review.")
        return redirect(url_for("patient_views.patient_profile_page"))

    return render_template("update_flagged_questionnaire.html", questionnaire=questionnaire, flagged_questions=flagged_questions, title="Update Flagged Questions")
