from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db
from App.controllers import *

anesthesiologist_views = Blueprint('anesthesiologist_views', __name__, template_folder='../templates')


'''
Page Routes
'''

@anesthesiologist_views.route('/dashboard/anesthesiologist', methods=['GET'])
@anesthesiologist_required
def anesthesiologist_dashboard_page():
    patients = get_all_patients()
    patient_questionnaires = get_all_questionnaires()
    return render_template('anesthesiologist_dashboard.html', patient_questionnaires=patient_questionnaires, patients=patients)


@anesthesiologist_views.route('/dashboard/anesthesiologist/patient/<patient_id>', methods=['GET'])
@anesthesiologist_required
def anesthesiologist_patient_info_page(patient_id):
    patient = get_patient_by_id(patient_id)
    return render_template('patient_info.html', patient=patient)

@anesthesiologist_views.route('/dashboard/anesthesiologist/questionnaire/<questionnaire_id>', methods=['GET'])
@anesthesiologist_required
def anesthesiologist_questionnaire_page(questionnaire_id):
    questionnaire = get_questionnaire(questionnaire_id)
    questions = get_default_questionnaire()
    return render_template('questionnaire_view.html', questionnaire=questionnaire, questions=questions)


'''
Action Routes
'''

@anesthesiologist_views.route('/dashboard/anesthesiologist/questionnaire/submit/<questionnaire_id>', methods=['POST'])
@anesthesiologist_required
def update_questionnaire_anesthesiologist_action(questionnaire_id):
    data = request.form   
    status = data['status']
    notes = data['anesthesiologist_notes']
    print(questionnaire_id, status, notes)

    if update_questionnaire_anesthesiologist(current_user.id, questionnaire_id, notes, status):
        flash('Comments added successfully')
    else:
        flash('Error adding notes')
    return redirect(request.referrer)


