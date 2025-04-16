from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db
from App.controllers import *
from datetime import datetime, date

patient_views = Blueprint('patient_views', __name__, template_folder='../templates')


'''
Page Routes
'''

@patient_views.route('/patient/profile', methods=['GET'])
@patient_required
def patient_profile_page():
    notifications = get_patient_notifications(current_user.id)
    if not current_user.med_history_updated:
        flash('Please update your Medical History to be able to fill out a questionnaire')
    medical_history = get_medical_history(current_user.id)
    return render_template('patient_account.html', notifications=notifications, medical_history=medical_history, title= 'Patient Profile', date=date)


'''
Action Routes
'''

@patient_views.route('/patient/medical_history', methods=['GET', 'POST'])
def manage_medical_history():
    if request.method == 'POST':
        data = request.form
        dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        blood_type = data['blood_type']
        weight = data['weight']
        height = data['height']
        gender = data['gender']
        allergies = data['allergies']
        medical_conditions = data['medical_conditions']
        medication = data['medication']
        
        age = calculate_age(dob)
        if create_medical_history(current_user.id, age, dob, gender, blood_type, weight, height, allergies, medical_conditions, medication):
            flash('Medical history added successfully')
        else:
            flash('Error adding medical history')
        return redirect('/patient/medical_history')
    
    medical_history = get_medical_history(current_user.id)
    return render_template('patient_account.html', medical_history=medical_history, title= 'Patient Account', date=date)


@patient_views.route('/seen/<notification_id>', methods=['POST'])
@patient_required
def seen_action(notification_id):
    reponse = seen_notification(notification_id)
    if reponse:
        return jsonify({'message': 'Notification seen'})
    return jsonify({'message': 'Notification not seen'}), 400

