from private_clinic.decorators import logout_required, employee_login_required
from flask_login import login_required, current_user
from private_clinic import services
from flask import request, jsonify
from private_clinic.app import app
from datetime import datetime


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
    data = request.json
    email = data.get('email')

    user = services.get_user_by_email(email=email)

    return jsonify({
        'status_code': 200 if not user else 400,
        'message': 'Account does not exist.' if not user else '',
    })


@login_required
def check_appointment_availability():
    data = request.json
    day_of_exam = data.get('day_of_exam')
    time_of_exam = data.get('time_of_exam')

    date_obj = datetime.strptime(day_of_exam, '%Y-%m-%d').date()
    time_obj = datetime.strptime(time_of_exam, '%H:%M').time()

    amount_patients_of_day = services.count_examination_schedule_by_date(date=date_obj)
    if amount_patients_of_day >= app.config['MAX_PATIENTS_PER_DAY']:
        return jsonify({
            'status_code': 401,
            'message': 'The number of registrations for the day has reached the maximum',
        })

    has_examination_schedule_at_time = services.check_examination_schedule_by_time(time=time_obj)
    if has_examination_schedule_at_time:
        return jsonify({
            'status_code': 402,
            'message': 'The time has been pre-registered by someone else',
        })

    return jsonify({
        'status_code': 200,
        'message': 'Successfully registered',
    })


@login_required
def check_profile_infor():
    data = request.json
    email = data.get('email')
    phone_number = data.get('phone_number')
    insurance_id = data.get('insurance_id')

    checks = [
        ('Email', 401, email, services.check_duplicate_email),
        ('Phone number', 402, phone_number, services.check_duplicate_phone_number),
        ('Insurance ID', 403, insurance_id, services.check_duplicate_insurance_id),
    ]

    for label, status_code, value, checker in checks:
        exists = checker(value, current_user_id=current_user.user.id)
        if exists:
            return jsonify({
                'status_code': status_code,
                'message': f'{label} is already linked to another account.',
            })

    return jsonify({
        'status_code': 200,
        'message': 'Saved successfully',
    })


# @employee_login_required
def load_examination_schedule_list_by_date():
    data = request.json
    day_of_exam = data.get('day_of_exam')

    date_obj = datetime.strptime(day_of_exam, '%Y-%m-%d').date()

    schedules = services.get_examination_schedule_list_by_date(date=date_obj)
    schedule_list = []
    for schedule in schedules:
        schedule_list.append({
            'id': schedule.id,
            'full_name': schedule.last_name + ' ' + schedule.first_name,
            'gender': schedule.gender,
            'dob': schedule.dob,
            'address': schedule.address,
        })

    return jsonify(schedule_list)
