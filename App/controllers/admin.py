from flask import Blueprint, render_template, request, redirect, url_for, flash
from App.models.admin import Admin
from App.models import User
from App.database import db
from App.controllers.doctor import create_doctor
from App.controllers.anesthesiologist import create_anesthesiologist
from App.controllers.doctor import delete_doctor
from App.controllers.anesthesiologist import delete_anesthesiologist

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

def create_admin(firstname, lastname, username, password, phone_number, email):
    new_admin = Admin(firstname=firstname, lastname=lastname, username=username, password=password, email=email, phone_number=phone_number)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin

@admin_blueprint.route('/')
def dashboard():
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@admin_blueprint.route('/add_staff', methods=['GET', 'POST'])
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
            return redirect(url_for('admin.add_staff'))

        if staff:
            flash('Staff added successfully.')
        else:
            flash('Error adding staff.')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin_add_staff.html')

@admin_blueprint.route('/remove_staff/<username>', methods=['POST'])
def remove_staff(username):
    if delete_doctor(username) or delete_anesthesiologist(username):
        flash('Staff removed successfully.')
    else:
        flash('Staff removal failed.')
    return redirect(url_for('admin.dashboard'))

@admin_blueprint.route('/reset_staff_password', methods=['GET', 'POST'])
def reset_staff_password():
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        user = User.query.filter_by(username=username).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            flash('Password reset successfully.')
        else:
            flash('User not found.')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin_reset_password.html')
