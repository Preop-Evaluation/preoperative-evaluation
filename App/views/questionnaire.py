from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
from App.controllers import *

questionnaire_views = Blueprint('questionnaire_views', __name__, template_folder='../templates')


@questionnaire_views.route('/questionnaire', methods=['GET', 'POST'])
@patient_required
def questionnaire_page():
    questions = get_default_questionnaire()
    if current_user.med_history_updated:
        latest_responses = None
        if current_user.autofill_enabled:
            latest_responses = get_latest_questionnaire(current_user.id).responses
            print(latest_responses)
        
        return render_template('questionnaire_form.html', questions=questions, latest_responses=latest_responses)
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
    return render_template('questionnaire_view.html', questions=questions, questionnaire=questionnaire)


@questionnaire_views.route('/submit_questionnaire', methods=['POST'])
@patient_required
def submit_questionnaire():
    questions = get_default_questionnaire()

    # Parsing form data and building a response dict
    responses = {}
    for key, value in request.form.items():
        if key.startswith('question_'):
            question_id = key.split('_')[1]
            responses[question_id] = value

    # Handle follow-up questions
    for question in questions:
        if question.get('follow_ups'):
            for follow_up in question['follow_ups']:
                follow_up_id = 'question_' + follow_up['id']
                if follow_up_id in request.form:
                    responses[follow_up['id']] = request.form[follow_up_id]

    # Save the responses to the database
    questionnaire = create_questionnaire(patient_id=current_user.id, responses=responses)
    if questionnaire:
        flash('Questionnaire submitted successfully!')
    else:
        flash('Error submitting questionnaire!')

    return render_template('questionnaire_view.html', questions=questions,  questionnaire=questionnaire)
    # return jsonify(responses), 200
