from private_clinic.app import db
from models import Account, User

import hashlib


def create_account(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(username=username.strip(), password=password)

    db.session.add(account)
    db.session.commit()

    return account
