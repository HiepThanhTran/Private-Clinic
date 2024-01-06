from flask import request, jsonify

from private_clinic import services
from private_clinic.decorators import logout_required


@logout_required
def check_signin_infor():
    data = request.json
    username_signin = data.get('username_signin')
    password_signin = data.get('password_signin')

    account = services.authenticate(username=username_signin, password=password_signin)

    return jsonify({
        'status_code': 200 if account else 400,
        'message': 'Username or password is incorrect.',
    })


@logout_required
def check_signup_infor():
    message = None
    data = request.json
    username_signup = data.get('username_signup')
    email_signup = data.get('email_signup')

    account = services.get_account_by_username(username_signup)
    user = services.get_user_by_email(email_signup)

    if account:
        message = 'Username is already in use.'
    elif user:
        message = 'Email is already linked to another account.'

    return jsonify({
        'status_code': 200 if not message else 400,
        'message': message,
    })


@logout_required
def check_account_exists():
    message = None
    data = request.json
    infor = data.get('infor')

    user = services.get_user_by_email(email=infor)

    if not user:
        message = 'Account does not exist.'

    return jsonify({
        'status_code': 200 if not message else 400,
        'message': message,
    })
