import getpass
from datetime import datetime

from flask.cli import FlaskGroup

from private_clinic import services
from private_clinic.app import app
from private_clinic.models import AccountRoleEnum


cli = FlaskGroup(app)


@cli.command('create_admin')
def create_admin():
    username = input("Enter username: ")
    email = input("Enter email address: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
    else:
        try:
            account = services.create_account(
                username=username,
                password=password,
                role=AccountRoleEnum.ADMIN,
                is_confirmed=True,
                confirmed_on=datetime.now())
            user = services.create_user(first_name=first_name, last_name=last_name, email=email, account_id=account.id)
            employee = services.create_employee(employee_id=user.id)
            admin = services.create_administrator(administrator_id=employee.id, inauguration_day=datetime.now())
            print(f"Admin with email {email} created successfully!")
        except:
            print("Couldn't create admin user.")


@cli.command('create_patient')
def create_patient():
    username = input('Enter username: ')
    email = input('Enter email address: ')
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    password = getpass.getpass('Enter password: ')
    confirm_password = getpass.getpass('Enter password again: ')
    if password != confirm_password:
        print("Passwords don't match")
    else:
        try:
            account = services.create_account(
                username=username,
                password=password,
                is_confirmed=True,
                confirmed_on=datetime.now()
            )
            user = services.create_user(first_name=first_name, last_name=last_name, email=email, account_id=account.id)
            patient = services.create_patient(patient_id=user.id)
            print(f'Patient with username {username} created successfully!')
        except:
            print("Couldn't create user.")


@cli.command('create_nurse')
def create_nurse():
    username = input('Enter username: ')
    email = input('Enter email address: ')
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    educational_attainment = input('Enter educational attainment: ')
    password = getpass.getpass('Enter password: ')
    confirm_password = getpass.getpass('Enter password again: ')
    if password != confirm_password:
        print("Passwords don't match")
    else:
        try:
            account = services.create_account(
                username=username,
                password=password,
                is_confirmed=True,
                confirmed_on=datetime.now()
            )
            user = services.create_user(first_name=first_name, last_name=last_name, email=email, account_id=account.id)
            employee = services.create_employee(employee_id=user.id)
            nurse = services.create_nurse(nurse_id=employee.id, educational_attainment=educational_attainment)
            print(f'Created successfully!')
        except:
            print("Couldn't create.")


@cli.command('create_cashier')
def create_cashier():
    username = input('Enter username: ')
    email = input('Enter email address: ')
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    password = getpass.getpass('Enter password: ')
    confirm_password = getpass.getpass('Enter password again: ')
    if password != confirm_password:
        print("Passwords don't match")
    else:
        try:
            account = services.create_account(
                username=username,
                password=password,
                is_confirmed=True,
                confirmed_on=datetime.now()
            )
            user = services.create_user(first_name=first_name, last_name=last_name, email=email, account_id=account.id)
            employee = services.create_employee(employee_id=user.id)
            cashier = services.create_cashier(cashier_id=employee.id)
            print(f'Created successfully!')
        except:
            print("Couldn't create.")


@cli.command('create_doctor')
def create_doctor():
    username = input('Enter username: ')
    email = input('Enter email address: ')
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    specialist = input('Enter specialist: ')
    years_of_experience = input('Enter years_of_experience: ')
    password = getpass.getpass('Enter password: ')
    confirm_password = getpass.getpass('Enter password again: ')
    if password != confirm_password:
        print("Passwords don't match")
    else:
        try:
            account = services.create_account(
                username=username,
                password=password,
                is_confirmed=True,
                confirmed_on=datetime.now()
            )
            user = services.create_user(first_name=first_name, last_name=last_name, email=email, account_id=account.id)
            employee = services.create_employee(employee_id=user.id)
            doctor = services.create_doctor(doctor_id=employee.id, specialist=specialist, years_of_experience=years_of_experience)
            print(f'Created successfully!')
        except:
            print("Couldn't create.")


if __name__ == '__main__':
    cli()
