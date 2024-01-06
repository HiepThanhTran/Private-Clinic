from private_clinic.app import app, mail
from private_clinic import dao
from flask_mail import Message


@app.context_processor
def common_response():
    return {

    }


def send_email(to, subject, template):
    return mail.send(Message(subject=subject, recipients=[to], html=template, sender=app.config['MAIL_DEFAULT_SENDER']))


def authenticate(username, password):
    return dao.authenticate(username=username, password=password)


def count_examination_schedule_by_date(date):
    return dao.count_examination_schedule_by_date(date=date)


def check_examination_schedule_by_time(time):
    return dao.check_examination_schedule_by_time(time=time)


def create_account(username, password):
    return dao.create_account(username=username, password=password)


def create_user(first_name, last_name, email, account_id):
    return dao.create_user(first_name=first_name, last_name=last_name, email=email, account_id=account_id)


def create_patient(patient_id):
    return dao.create_patient(patient_id=patient_id)


def create_employee(employee_id):
    return dao.create_employee(employee_id=employee_id)


def create_administrator(administrator_id):
    return dao.create_administrator(administrator_id=administrator_id)


def create_cashier(cashier_id):
    return dao.create_cashier(cashier_id=cashier_id)


def create_nurse(nurse_id):
    return dao.create_nurse(nurse_id=nurse_id)


def create_doctor(doctor_id):
    return dao.create_doctor(doctor_id=doctor_id)


def create_examination_schedule(patient_id, examination_date, **kwargs):
    return dao.create_examination_schedule(patient_id=patient_id, examination_date=examination_date, **kwargs)


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
