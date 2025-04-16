from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db
from App.models import *
from App.controllers import *

admin_views = Blueprint('admin_views', __name__, template_folder='../templates', url_prefix='/admin')

@admin_views.route('/')
def dashboard():
    doctors = Doctor.query.all()
    anesthesiologists = Anesthesiologist.query.all()
    patients = Patient.query.all()
    admins = Admin.query.all()

    users = doctors + anesthesiologists + patients + admins

    return render_template('admin_dashboard.html', users=users, title= 'Admin Dashboard')


@admin_views.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
        role = request.form.get('role')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')

        if role == 'doctor':
            staff = create_doctor(firstname, lastname, username, password, email, phone_number)
        elif role == 'anesthesiologist':
            staff = create_anesthesiologist(firstname, lastname, username, password, email, phone_number)
        else:
            flash('Invalid staff role selected')
            return redirect(url_for('admin_views.add_staff'))

        if staff:
            flash('Staff added successfully.')
        else:
            flash('Error adding staff.')
        return redirect(url_for('admin_views.dashboard'))

    return render_template('admin_add_staff.html', title='Add Staff')

@admin_views.route('/remove_staff/<username>', methods=['POST'])
def remove_staff(username):
    if delete_doctor(username) or delete_anesthesiologist(username) or delete_patient(username):
        flash('User removed successfully.')
    else:
        flash('User removal failed.')
    return redirect(url_for('admin_views.dashboard'))

@admin_views.route('/reset_staff_password', methods=['GET', 'POST'])
def reset_staff_password():
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        
        user = Doctor.query.filter_by(username=username).first()
        if not user:
            user = Anesthesiologist.query.filter_by(username=username).first()
        if not user:    
            user = Patient.query.filter_by(username=username).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            flash('Password reset successfully.')
        else:
            flash('User not found.')
        return redirect(url_for('admin_views.dashboard'))
    return render_template('admin_reset_password.html', title='Reset Staff Password')
