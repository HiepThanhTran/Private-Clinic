from datetime import datetime

from flask import request, jsonify
from flask_login import login_required, current_user

from private_clinic import services
from private_clinic.app import app
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
    data = request.json
    email = data.get('email')

    user = services.get_user_by_email(email=email)

    return jsonify({
        'status_code': 200 if user else 400,
        'message': 'Account does not exist.' if not user else 'Account exists.',
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

    schedules = services.get_examination_schedules_list_by_date(date=date_obj)
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


def load_medicines_list():
    medicines = services.get_medicines_list()
    medicine_list = []
    for medicine in medicines:
        medicine_list.append({
            'id': medicine.id,
            'medicine_name': medicine.medicine_name,
            'medicine_unit': medicine.medicine_unit.unit_name,
            'direction_for_use': medicine.direction_for_use
        })

    return jsonify(medicine_list)


def load_packages_list():
    packages_load = services.get_packages_list()
    packges_list = []
    for packages in packages_load:
        packges_list.append({
            'id': packages.id,
            'packages_name': packages.packages_name,
        })

    return jsonify(packges_list)


def load_medicines_list_by_medical_bill_id():
    prescriptions = services.get_details_bill()

    prescriptions_list = []
    for prescription in prescriptions:
        prescriptions_list.append({
            'id': prescription.id,
            'medicine_name': prescription.medicine_name,
            'medicine_unit': prescription.unit_name,
            'amount': prescription.amount,
            'direction_for_use': prescription.direction_for_use,
            'medical_bill_id': prescription.medical_bill_id,
            'medicine_price': prescription.medicine_price,
            'package_price': prescription.package_price,
        })

    return jsonify(prescriptions_list)


def load_chart_stats_medicine_by_month():
    data = request.json
    month = data.get('month')
    medicine_name = data.get('medicine_name')
    date_obj = datetime.strptime(month, '%Y-%m').date() if month else None

    medicine_stats = services.stats_medicine_usage_per_month(month=date_obj.month if month else None, medicine_name=medicine_name)
    medicine_stats_json = []

    for medicine in medicine_stats:
        medicine_stats_json.append({
            'month': medicine.month,
            'medicine_name': medicine.medicine_name,
            'unit_name': medicine.unit_name,
            'amount': medicine.amount,
            'usage_count': medicine.usage_count
        })

    return jsonify(medicine_stats_json)
