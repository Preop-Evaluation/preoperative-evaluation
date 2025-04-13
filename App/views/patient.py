from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db
from App.controllers import *


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
    return render_template('patient_account.html', notifications=notifications, title= 'Patient Profile')


'''
Action Routes
'''

@patient_views.route('/patient/medical_history', methods=['GET', 'POST'])
def manage_medical_history():
    if request.method == 'POST':
        data = request.form
        age = data['age']
        blood_type = data['blood_type']
        weight = data['weight']
        height = data['height']
        allergies = data['allergies']
        medical_conditions = data['medical_conditions']
        medication = data['medication']
        
        if create_medical_history(current_user.id, age, blood_type, weight, height, allergies, medical_conditions, medication):
            flash('Medical history added successfully')
        else:
            flash('Error adding medical history')
        return redirect(request.referrer)
    
    medical_history = get_medical_history(current_user.id)
    return render_template('patient_account.html', medical_history=medical_history, title= 'Patient Account')


@patient_views.route('/seen/<notification_id>', methods=['POST'])
@patient_required
def seen_action(notification_id):
    reponse = seen_notification(notification_id)
    if reponse:
        return jsonify({'message': 'Notification seen'})
    return jsonify({'message': 'Notification not seen'}), 400

