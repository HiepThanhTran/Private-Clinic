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


if __name__ == '__main__':
    cli()
