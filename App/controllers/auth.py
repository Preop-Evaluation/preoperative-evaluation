from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
from flask import render_template

from App.models import User, Doctor, Anesthesiologist, Patient

from functools import wraps


def jwt_authenticate(username, password):
    user = Patient.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)
    
    user = Doctor.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)

    user = Anesthesiologist.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)

    return None

def login(username, password):
    user = Patient.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)

    user = Doctor.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)

    user = Anesthesiologist.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)
    return None

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        user = Doctor.query.get(user_id)

        if user:
            return user
        
        user = Anesthesiologist.query.get(user_id)

        if user:
            return user

        return Patient.query.get(user_id)
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):

        user = Doctor.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id

        user = Anesthesiologist.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id

        user = Patient.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return Patient.query.get(identity)

    return jwt

    #Edits below

#Login actions
def login_anesthesiologist(username, password):
    manager = Anesthesiologist.query.filter_by(username = username).first()

    if manager and manager.check_password(password):
        login_user(manager)
        return manager
    return None   

def login_doctor(username, password):
    doctor = Doctor.query.filter_by(username = username).first()

    if doctor and doctor.check_password(password):
        login_user(doctor)
        return doctor
    return None

def login_patient(name,password):
    patient = Patient.query.filter_by(username = name).first()

    if patient and patient.check_password(password):
        login_user(patient)
        return patient
    return None

#Logout action
def logout():
    logout_user()

#Wrappers
def anesthesiologist_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Anesthesiologist):
            return render_template("unauthorized.html"), 401
        return func(*args, **kwargs)
    return wrapper

def doctor_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Doctor):
            return render_template("unauthorized.html"), 401
        return func(*args, **kwargs)
    return wrapper

def patient_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):        
        if not  current_user.is_authenticated or not isinstance(current_user, Patient):
            return render_template("unauthorized.html"), 401
        return func(*args, **kwargs)
    return wrapper

# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          user_id = get_jwt_identity()
          current_user = User.query.get(user_id)
          is_authenticated = True
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)