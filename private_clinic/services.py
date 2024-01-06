from flask_mail import Message

from private_clinic import dao
from private_clinic.app import app, mail


def authenticate(username, password):
    return dao.authenticate(username=username, password=password)


def create_account(username, password):
    return dao.create_account(username=username, password=password)


def create_user(first_name, last_name, email, account_id):
    return dao.create_user(first_name=first_name, last_name=last_name, email=email, account_id=account_id)


def create_patient(patient_id):
    return dao.create_patient(patient_id=patient_id)


def update_account_password(account_id, new_password):
    return dao.update_account_password(account_id=account_id, new_password=new_password)


def get_account_by_id(account_id):
    return dao.get_account_by_id(account_id=account_id)


def get_account_by_username(username):
    return dao.get_account_by_username(username=username)


def get_account_by_email(email):
    return dao.get_account_by_email(email=email)


def get_account_by_phone_number(phone_number):
    return dao.get_account_by_phone_number(phone_number=phone_number)


def get_user_by_email(email):
    return dao.get_user_by_email(email=email)


def send_email(to, subject, template):
    msg = Message(subject=subject, recipients=[to], html=template, sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)
