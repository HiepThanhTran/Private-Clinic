from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import login_required, current_user, login_user, logout_user

from private_clinic import services
from private_clinic.app import db, login, app
from private_clinic.decorators import logout_required, check_is_confirmed, employee_logout_required
from private_clinic.services import send_email
from private_clinic.token import confirm_token, generate_token


# --------------------RENDER FUNCTIONS-------------------- #
@app.context_processor
def common_response():
    return {

    }


def index():
    return render_template(template_name_or_list='index.html')


def about():
    return render_template(template_name_or_list='about.html')


def healthcare_staff():
    return render_template(template_name_or_list='healthcare_staff.html')


def medicine():
    return render_template(template_name_or_list='customer/medicine.html')


# @employee_login_required
def employee():
    return render_template(template_name_or_list='employee/employee_home.html')


@logout_required
def authentication():
    return render_template(template_name_or_list='authentication.html')


@logout_required
def password_reset(token):
    return render_template(template_name_or_list='customer/password_reset.html', token=token)


def notification():
    if not get_flashed_messages():
        return redirect(url_for('index'))

    return render_template(template_name_or_list='notification.html')


# --------------------AUTHENTICATION-------------------- #
@login.user_loader
def account_load(account_id):
    return services.get_account_by_id(account_id)


@logout_required
def signin():
    if request.method.__eq__('POST'):
        next_url = request.form.get('next')
        username_signin = request.form.get('username_signin')
        password_signin = request.form.get('password_signin')

        account = services.authenticate(username=username_signin, password=password_signin)

        login_user(account)
        return redirect('/' if next_url is None else next_url)


@logout_required
def signup():
    if request.method.__eq__('POST'):
        username = request.form.get('username_signup')
        password = request.form.get('password_signup')
        first_name = request.form.get('firstname_signup')
        last_name = request.form.get('lastname_signup')
        email = request.form.get('email_signup')

        account = services.create_account(username=username, password=password)
        user = services.create_user(first_name=first_name, last_name=last_name, email=email, account_id=account.id)
        patient = services.create_patient(patient_id=user.id)

        token = generate_token(user.email)
        subject = 'Please confirm your email'
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('mail/confirm_email.html', confirm_url=confirm_url)
        send_email(to=user.email, subject=subject, template=html)

        login_user(account)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for('notification'))


@logout_required
def forgot_password():
    if request.method.__eq__('POST'):
        email = request.form.get('email')

        subject = "Password reset requested"
        token = generate_token(email)
        recovery_url = url_for('password_reset', token=token, _external=True)
        html = render_template('mail/password_reset_email.html', recovery_url=recovery_url)
        send_email(to=email, subject=subject, template=html)

        flash('The reset request has been sent to via email.', 'success')
        return redirect(url_for('notification'))


@logout_required
def reset_with_token(token):
    if request.method.__eq__('POST'):
        email = confirm_token(token)
        user = services.get_user_by_email(email=email)

        if user.email != email:
            flash('The request link is invalid or has expired.', 'danger')
        else:
            new_password = request.form.get('new_password')

            services.update_account_password(account_id=user.account_id, new_password=new_password)
            flash('Password updated', 'success')

        return redirect(url_for('notification'))


@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))


# --------------------CUSTOMER FUNCTIONS-------------------- #
@login_required
@check_is_confirmed
def appointment():
    if request.method.__eq__('POST'):
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        day_of_exam = request.form.get('day_of_exam')
        time_of_exam = request.form.get('time_of_exam')

        date_obj = datetime.strptime(day_of_exam, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_of_exam, '%H:%M').time()
        combined_datetime = datetime.combine(date_obj, time_obj)

        examination_schedule = services.create_examination_schedule(
            patient_id=current_user.user.id,
            examination_date=combined_datetime,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            gender=gender,
            email=email,
            phone_number=phone_number,
            address=address)

        flash('Successfully registered for examination appointment, please wait for confirmation information to be sent via phone number',
              'success')
        return redirect(url_for('notification'))

    return render_template(template_name_or_list='customer/appointment.html')


@login_required
def profile_settings(slug):
    if request.method.__eq__('POST'):
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        insurance_id = request.form.get('insurance_id')
        avatar = request.files.get('avatar')

        user = services.update_profile_user(
            user_id=current_user.user.id,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            gender=gender,
            email=email,
            phone_number=phone_number,
            address=address,
            insurance_id=insurance_id,
            avatar=avatar)
        flash('Saved successfully.', 'success')

    return render_template(template_name_or_list='customer/profile_settings.html')


@login_required
def account_settings(slug):
    return render_template(template_name_or_list='customer/account_settings.html')


# --------------------EMPLOYEE-------------------- #
@employee_logout_required
def employee_login():
    return render_template(template_name_or_list='employee/login.html')


# @employee_login_required
# @check_role(AccountRoleEnum.NURSE)
def employee_nurse():
    if request.method.__eq__('POST'):
        day_of_exam = request.form.get('day_of_exam')
        schedules = request.form.getlist('examination_id')

        examination_list = services.create_examination_list(examination_date=day_of_exam, nurse_id=current_user.user.employee.nurse.id,
                                                            examination_schedule_id_list=schedules)

        flash('Create an examination list and send notifications to patients successfully', 'success')
        return redirect(url_for('employee_nurse'))

    examination_schedule_list = services.get_examination_schedule_list()

    return render_template(template_name_or_list='employee/nurse.html', examination_schedule_list=examination_schedule_list)


# @employee_login_required
# @check_role(AccountRoleEnum.DOCTOR)
def employee_doctor():
    return render_template(template_name_or_list='employee/doctor.html')


# @employee_login_required
# @check_role(AccountRoleEnum.STAFF)
def employee_cashier():
    return render_template(template_name_or_list='employee/cashier.html')


def admin_dashboard():
    return render_template(template_name_or_list='admin/dashboard.html')


def admin_analytics():
    return render_template(template_name_or_list='admin/analytics.html')


# --------------------VERIFY EMAIL-------------------- #
@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        flash('Account already confirmed.', 'success')
        return redirect(url_for('index'))

    email = confirm_token(token)
    user = services.get_user_by_email(email=current_user.user.email)

    if user.email != email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('notification'))

    account = services.get_account_by_id(account_id=user.account_id)

    account.is_confirmed = True
    account.confirmed_on = datetime.now()

    db.session.add(account)
    db.session.commit()

    flash('You have confirmed your account. Thanks!', 'success')

    return redirect(url_for('notification'))


@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        flash('Your account has already been confirmed.', 'success')
        return redirect(url_for('index'))

    token = generate_token(current_user.user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('mail/confirm_email.html', confirm_url=confirm_url)
    subject = 'Please confirm your email'
    send_email(current_user.user.email, subject, html)

    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('notification'))
