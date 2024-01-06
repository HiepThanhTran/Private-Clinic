from private_clinic.models import Account, User, Patient
from private_clinic.app import db
import hashlib


def authenticate(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return Account.query.filter(Account.username.__eq__(username.strip()), Account.password.__eq__(password)).first()


def create_account(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(username=username.strip(), password=password)

    db.session.add(account)
    db.session.commit()

    return account


def create_user(first_name, last_name, email, account_id):
    user = User(first_name=first_name.strip(), last_name=last_name.strip(), email=email.strip(), account_id=account_id)

    db.session.add(user)
    db.session.commit()

    return user


def create_patient(patient_id):
    patient = Patient(id=patient_id)

    db.session.add(patient)
    db.session.commit()

    return patient


def update_account_password(account_id, new_password):
    new_password = str(hashlib.md5(new_password.strip().encode('utf-8')).hexdigest())

    account = Account.query.get(account_id)
    account.password = new_password
    db.session.commit()

    return account


def get_account_by_id(account_id):
    return Account.query.get(account_id)


def get_account_by_username(username):
    return Account.query.filter_by(username=username).first()
    # return db.session.query(db.session.query(Account).filter_by(username=username).exists()).scalar()


def get_account_by_email(email):
    return Account.query.join(User).filter_by(email=email).first()


def get_account_by_phone_number(phone_number):
    return Account.query.join(User).filter_by(phone_number=phone_number).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
    # return db.session.query(db.session.query(User).filter_by(email=email).exists()).scalar()
