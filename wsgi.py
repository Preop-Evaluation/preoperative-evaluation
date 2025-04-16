import click, pytest, sys
from flask import Flask, render_template
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():    
    initialize_db()


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

'''
User Commands
'''

user_cli = AppGroup('user', help='User object commands') 
doctor_cli = AppGroup('doctor', help='Doctor-related commands')
admin_cli = AppGroup('admin', help='Admin-related commands')
patient_cli = AppGroup('patient', help='Patient object commands')
questionnaire_cli = AppGroup('questionnaire', help='Questionnaire object commands')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_patients())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

#command to list an admin
@admin_cli.command("list", help="Lists all admins")
def list_admins():
    admins = get_all_admins()
    
    if not admins:
        print("No admins found.")
        return

    print("\nAdmin List:")
    print("-" * 40)

    for admin in admins: 
        print(f"ID: {admin['id']}, Name: {admin['name']}, Username: {admin['username']}, Role: {admin['role']}, Email: {admin['email']}")

#command to create an admin
@admin_cli.command("create", help="Creates an admin")
@click.argument("firstname", default="rob")
@click.argument("lastname", default="rob")
@click.argument("username", default="rob")
@click.argument("password", default="rob")
@click.argument("email", default="rob")
@click.argument("phone_number", default="rob")
def create_admin_command(firstname, lastname, username, password, email, phone_number):  
    admin = create_admin(firstname, lastname, username, password, email, phone_number)  
    print(f'{admin.firstname} created!')
app.cli.add_command(admin_cli)

#command to delete an admin
@admin_cli.command("delete", help="Deletes an admin by username")
@click.argument("username", type=str)
def delete_admin_command(username):
    if delete_admin(username):
        print(f"Admin with username {username} deleted successfully.")
    else:
        print(f"Failed to delete admin with username {username}.")


#command to create a patient
@patient_cli.command("create", help="Creates a patient")
@click.argument("firstname", default="rob")
@click.argument("lastname", default="rob")
@click.argument("username", default="rob")
@click.argument("password", default="rob")
@click.argument("email", default="rob")
@click.argument("phone_number", default="rob")
def create_patient_command(firstname, lastname, username, password, email, phone_number):  
    patient = create_patient(firstname, lastname, username, password, email, phone_number)  
    print(f'{patient.firstname} created!')

#command to add medical history for a patient by name
@patient_cli.command("create_history", help="Creates medical history for a patient")
@click.argument("firstname")
@click.argument("lastname")
@click.argument("age", default=30)
@click.argument("blood_type", default="O+")
@click.argument("weight", default=70.0)
@click.argument("height", default=175)
@click.argument("gender", default="Male")
@click.argument("allergies", default="None")
@click.argument("medical_conditions", default="None")
@click.argument("medication", default="None")
def create_medical_history_command(firstname, lastname, age, gender, blood_type, weight, height, allergies, medical_conditions, medication):
    patient = Patient.query.filter_by(firstname=firstname, lastname=lastname).first()
    
    if not patient:
        print(f"Error: Patient with name {firstname} {lastname} not found.")
        return
    user = create_medical_history(patient.id, age, gender, blood_type, weight, height, allergies, medical_conditions, medication)
    
    if user:
        print(f"Medical history for patient {patient.firstname} {patient.lastname} created!")
    else:
        print("Error creating medical history.")

@patient_cli.command("display_data", help="Displays all patient data given firstname and lastname")
@click.argument("firstname")
@click.argument("lastname")
def display_patient_data_command(firstname, lastname):
    patient = Patient.query.filter_by(firstname=firstname, lastname=lastname).first()

    if not patient:
        print(f"Error: Patient with name {firstname} {lastname} not found.")
        return

    print(f"Patient Data:")
    print(f"Name: {patient.firstname} {patient.lastname}")
    print(f"Age: {patient.age}")
    print(f"Gender: {patient.gender}")
    print(f"Blood Type: {patient.blood_type}")
    print(f"Weight: {patient.weight} kg")
    print(f"Height: {patient.height} cm")
    print(f"Allergies: {patient.allergies}")
    print(f"Medical Conditions: {patient.medical_conditions}")
    print(f"Medication: {patient.medication}")


#command to list patients
@patient_cli.command("list", help="Lists all patients")
def list_patients():
    patients = get_all_patients()
    
    if not patients:
        print("No patients found.")
        return

    print("\nPatient List:")
    print("-" * 40)

    for patient in patients:
        print(f"ID: {patient.id}, Name: {patient.firstname} {patient.lastname}, Username: {patient.username}, email: {patient.email}")

#command to create a doctor
@doctor_cli.command("create", help="Creates a doctor")
@click.argument("firstname", default="John")
@click.argument("lastname", default="Doe")
@click.argument("username", default="johndoe")
@click.argument("password", default="password")
@click.argument("email", default="johndoe@example.com")
@click.argument("phone_number", default="1234567890")
def create_doctor_command(firstname, lastname, username, password, email, phone_number):
    doctor = create_doctor(firstname, lastname, username, password, email, phone_number)
    print(f'Doctor {doctor.firstname} {doctor.lastname} created!')

#Command to create an anesthesiologist
@doctor_cli.command("create_anest", help="Creates an anesthesiologist")
@click.argument("firstname", default="Jane")
@click.argument("lastname", default="Smith")
@click.argument("username", default="janesmith")
@click.argument("password", default="password")
@click.argument("email", default="janesmith@example.com")
@click.argument("phone_number", default="9876543210")
def create_anesthesiologist_command(firstname, lastname, username, password, email, phone_number):
    anesthesiologist = create_anesthesiologist(firstname, lastname, username, password, email, phone_number)
    print(f'Anesthesiologist {anesthesiologist.firstname} {anesthesiologist.lastname} created!')

#command to delete a doctor given their username
@doctor_cli.command("delete", help="Deletes a doctor by username")
@click.argument("username", type=str)
def delete_doctor_command(username):
    if delete_doctor(username):
        print(f"Doctor with username {username} deleted successfully.")
    else:
        print(f"Failed to delete doctor with username {username}.")

#command to delete an anesthesiologist given their username
@doctor_cli.command("delete_anesthesiologist", help="Deletes an anesthesiologist by username")
@click.argument("username", type=str)
def delete_anesthesiologist_command(username):
    if delete_anesthesiologist(username):
        print(f"Anesthesiologist with username {username} deleted successfully.")
    else:
        print(f"Failed to delete anesthesiologist with username {username}.")

#command to list all medical staff
@doctor_cli.command("list", help="Lists all medical staff")
def list_medical_staff():
    doctors = get_all_doctors()
    anesthesiologists = get_all_anesthesiologists()
    
    if not doctors and not anesthesiologists:
        print("No medical staff found.")
        return

    print("\nMedical Staff List:")
    print("-" * 40)
    
    for doctor in doctors:
        print(f"ID: {doctor['id']}, Name: {doctor['name']}, Username: {doctor['username']}, Role: {doctor['role']}, Email: {doctor['email']}")
    
    for anesthesiologist in anesthesiologists:
        print(f"ID: {anesthesiologist['id']}, Name: {anesthesiologist['name']}, Username: {anesthesiologist['username']}, Role: {anesthesiologist['role']}, Email: {anesthesiologist['email']}")

#command to update a doctor's info
@doctor_cli.command("update", help="Updates a doctor's information")
@click.argument("username", type=str)
@click.option("--firstname", type=str)
@click.option("--lastname", type=str)
@click.option("--new_username", type=str)
@click.option("--password", type=str)
@click.option("--email", type=str)
@click.option("--phone_number", type=str)
def update_doctor_command(username, firstname, lastname, new_username, password, email, phone_number):
    doctor = update_doctor(username, firstname, lastname, new_username, password, email, phone_number)
    if doctor:
        print(f"Doctor '{username}' updated successfully.")
    else:
        print(f"Failed to update doctor '{username}'.")
 
#command to update an anesth's info
@doctor_cli.command("update_anesthesiologist", help="Updates an anesthesiologist's information")
@click.argument("username", type=str)
@click.option("--firstname", type=str)
@click.option("--lastname", type=str)
@click.option("--new_username", type=str)
@click.option("--password", type=str)
@click.option("--email", type=str)
@click.option("--phone_number", type=str)
def update_anesthesiologist_command(username, firstname, lastname, new_username, password, email, phone_number):
    anesthesiologist = update_anesthesiologist(username, firstname, lastname, new_username, password, email, phone_number)
    
    if anesthesiologist:
        print(f"Anesthesiologist '{username}' updated successfully.")
    else:
        print(f"Failed to update anesthesiologist '{username}'.")

#command to get all questionnaires
@questionnaire_cli.command("list", help="Lists all questionnaires")
def list_questionnaires():
    questionnaires=get_all_questionnaires()

    if not questionnaires:
        print("No questionnaires found.")
        return

    print("\nQuestionnaires List:")
    print("-" * 40)
    
    for questionnaire in questionnaires:
        print(f"ID: {questionnaire.id}, Response: {questionnaire.responses}, Flagged: {questionnaire.flagged_questions}")
    
#command to edit a flagged question in a questionnaire
@questionnaire_cli.command("edit_flagged", help="Edits a flagged question")
@click.argument("questionnaire_id")
@click.argument("question_id")
@click.argument("new_answer")
def edit_flagged_question_command(questionnaire_id, question_id, new_answer):
    questionnaire = get_questionnaire(questionnaire_id)
    
    if not questionnaire:
        print(f"Error: Questionnaire with ID {questionnaire_id} not found.")
        return
    
    if question_id not in questionnaire.flagged_questions:
        print(f"Error: Question {question_id} is not flagged.")
        return
    
    print("Before Update:", questionnaire.responses)
    
    #the database was being quirky, so i ended up copying the responses to a new dict and then updating the questionnaire
    updated_responses = questionnaire.responses.copy()  
    updated_responses[question_id] = new_answer          
    questionnaire.responses = updated_responses          
    
    print("After Update: ", questionnaire.responses)
    
    try:
        db.session.commit()
        print(f"Flagged question {question_id} in questionnaire {questionnaire_id} updated to '{new_answer}'.")
    except Exception as e:
        print(f"Error during commit: {e}")
        db.session.rollback()

@questionnaire_cli.command("edit_followup", help="Edits a flagged follow-up question in a questionnaire")
@click.argument("questionnaire_id")
@click.argument("followup_id")
@click.argument("new_answer")
def edit_flagged_followup_command(questionnaire_id, followup_id, new_answer):
    questionnaire = get_questionnaire(questionnaire_id)
    
    if not questionnaire:
        print(f"Error: Questionnaire with ID {questionnaire_id} not found.")
        return
    
    print("Before Update:", questionnaire.responses)
    
    updated_responses = questionnaire.responses.copy() if questionnaire.responses else {}
    updated_responses[followup_id] = new_answer          
    questionnaire.responses = updated_responses          
    
    print("After Update:", questionnaire.responses)
    
    try:
        db.session.commit()
        print(f"Follow-up question {followup_id} in questionnaire {questionnaire_id} updated to '{new_answer}'.")
    except Exception as e:
        print(f"Error during commit: {e}")
        db.session.rollback()


app.cli.add_command(patient_cli)
app.cli.add_command(doctor_cli)
app.cli.add_command(questionnaire_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
