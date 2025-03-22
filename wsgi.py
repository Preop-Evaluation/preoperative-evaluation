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

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_patients())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

patient_cli = AppGroup('patient', help='Patient object commands')

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

app.cli.add_command(patient_cli)

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
    from App.controllers.doctor import get_all_doctors
    from App.controllers.anesthesiologist import get_all_anesthesiologists

    doctors = get_all_doctors()
    anesthesiologists = get_all_anesthesiologists()
    
    if not doctors and not anesthesiologists:
        print("No medical staff found.")
        return

    print("\nMedical Staff List:")
    print("-" * 40)
    
    for doctor in doctors:
        print(f"ID: {doctor['id']}, Name: {doctor['name']}, Username: {doctor['username']}, Role: {doctor['role']}")
    
    for anesthesiologist in anesthesiologists:
        print(f"ID: {anesthesiologist['id']}, Name: {anesthesiologist['name']}, Username: {anesthesiologist['username']}, Role: {anesthesiologist['role']}")

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
    from App.controllers.doctor import update_doctor

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
    from App.controllers.anesthesiologist import update_anesthesiologist

    anesthesiologist = update_anesthesiologist(username, firstname, lastname, new_username, password, email, phone_number)
    if anesthesiologist:
        print(f"Anesthesiologist '{username}' updated successfully.")
    else:
        print(f"Failed to update anesthesiologist '{username}'.")


app.cli.add_command(doctor_cli)

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
