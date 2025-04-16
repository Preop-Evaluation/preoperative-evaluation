from flask import Blueprint, render_template, request, redirect, url_for, flash
from App.models.admin import Admin
from App.models.user import User
from App.models import User
from App.database import db

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

def create_admin(firstname, lastname, username, password, phone_number, email):
    new_admin = Admin(firstname=firstname, lastname=lastname, username=username, password=password, email=email, phone_number=phone_number)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin

def get_all_admins():
    admins = Admin.query.all() 
    return [
        {
            "id": admin.id,
            "name": f"{admin.firstname} {admin.lastname}",
            "username": admin.username,
            "email": admin.email,
            "role": "Admin"
        }
        for admin in admins  
    ]

def delete_admin(username):
    try:
        admin_user = Admin.query.filter_by(username=username).first()
        if not admin_user:
            print(f"Admin with username '{username}' not found.")
            return False

        db.session.delete(admin_user)
        db.session.commit()
        print(f"Admin {admin_user.firstname} {admin_user.lastname} deleted successfully.")
        return True
    except Exception as e:
        print(f"{e} - Error deleting admin")
        return False
