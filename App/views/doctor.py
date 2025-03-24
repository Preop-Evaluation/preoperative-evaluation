from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db
from App.controllers import *
import datetime


doctor_views = Blueprint('doctor_views', __name__, template_folder='../templates')

'''
Page Routes
'''


@doctor_views.route('/dashboard/doctor', methods=['GET'])
@doctor_required
def doctor_dashboard_page():
    patients = get_all_patients()
    patient_questionnaires = get_all_questionnaires()
    return render_template('doctor_dashboard.html', patient_questionnaires=patient_questionnaires, patients=patients)

@doctor_views.route('/dashboard/doctor/patient/<patient_id>', methods=['GET'])
@doctor_required
def doctor_patient_info_page(patient_id):
    patient = get_patient_by_id(patient_id)
    return render_template('patient_info.html', patient=patient)

@doctor_views.route('/dashboard/doctor/questionnaire', methods=['GET'])
@doctor_required
def doctor_questionnaire_page():
    questionnaire_id = request.args.get('questionnaire_id')
    questionnaire = get_questionnaire(questionnaire_id)
    questions = get_default_questionnaire()
    return render_template('questionnaire_view.html', questionnaire=questionnaire, questions=questions)


'''
Action Routes
'''

@doctor_views.route('/dashboard/doctor/questionnaire/submit/<questionnaire_id>', methods=['POST'])
def update_questionnaire_doctor_action(questionnaire_id):
    data = request.form    
    operation_date = data['operation_date']
    notes = data['doctor_notes']
    print(questionnaire_id, operation_date, notes)
    
    if update_questionnaire_doctor(current_user.id, questionnaire_id, notes, operation_date):
        flash('Notes added successfully')
    else:
        flash('Error adding notes')
    return redirect(request.referrer)
