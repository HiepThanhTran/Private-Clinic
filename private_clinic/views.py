from flask import render_template, request, redirect, url_for, flash, get_flashed_messages, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from private_clinic.decorators import logout_required, check_is_confirmed
from private_clinic.token import confirm_token, generate_token
from private_clinic.services import send_email
from private_clinic.app import db, login, app
from private_clinic import services
from datetime import datetime


def index():
    return render_template(template_name_or_list='index.html')


def about():
    return render_template(template_name_or_list='about.html')


def nurse():
    return render_template(template_name_or_list='nurse.html')


def doctor():
    return render_template(template_name_or_list='doctor.html')


def cashier():
    return render_template(template_name_or_list='cashier.html')


def healthcare_staff():
    return render_template(template_name_or_list='healthcare_staff.html')


@logout_required
def authentication():
    return render_template(template_name_or_list='auth.html')


def medicine():
    return render_template(template_name_or_list='medicine.html')


@login_required
@check_is_confirmed
def appointment():
    if request.method.__eq__('POST'):
        status_code = 200
        message = ('Successfully registered for examination appointment, please wait for confirmation information to be sent via phone '
                   'number')

        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        dob = data.get('dob')
        gender = data.get('gender')
        email = data.get('email')
        phone_number = data.get('phone_number')
        address = data.get('address')
        day_of_exam = data.get('day_of_exam')
        time_of_exam = data.get('time_of_exam')

        date_obj = datetime.strptime(day_of_exam, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_of_exam, '%H:%M').time()
        combined_datetime = datetime.combine(date_obj, time_obj)

        amount_patients_of_day = services.count_examination_schedule_by_date(date=date_obj)

        if amount_patients_of_day < app.config['MAX_PATIENTS_PER_DAY']:
            has_examination_schedule_at_time = services.check_examination_schedule_by_time(time=time_obj)

            if has_examination_schedule_at_time is False:
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
            else:
                status_code = 402
                message = 'The time has been pre-registered by someone else'
        else:
            status_code = 401
            message = 'The number of registrations for the day has reached the maximum'

        return jsonify({
            'status_code': status_code,
            'message': message,
        })

    return render_template(template_name_or_list='appointment.html')


@login_required
def profile_settings():
    return render_template(template_name_or_list='profile_settings.html')


@logout_required
def password_reset(token):
    return render_template(template_name_or_list='password_reset.html', token=token)


@login.user_loader
def account_load(account_id):
    return services.get_account_by_id(account_id)


@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))


@logout_required
def signin():
    if request.method.__eq__('POST'):
        next_url = request.form.get('next')
        print(next_url)
        username_signin = request.form.get('username_signin')
        password_signin = request.form.get('password_signin')

        account = services.authenticate(username=username_signin, password=password_signin)

        login_user(account)
        return redirect('/' if next_url is None else next_url)


@logout_required
def forgot_password():
    if request.method.__eq__('POST'):
        infor_forgotpassword = request.form.get('infor_forgotpassword')

        subject = "Password reset requested"
        token = generate_token(infor_forgotpassword)
        recovery_url = url_for('password_reset', token=token, _external=True)
        html = render_template('mail/password_reset_email.html', recovery_url=recovery_url)
        send_email(to=infor_forgotpassword, subject=subject, template=html)

        flash('The reset request has been sent to via email.', 'success')
        return redirect(url_for('inactive'))


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

        return redirect(url_for('inactive'))


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
        return redirect(url_for('inactive'))


@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        flash('Account already confirmed.', 'success')
        return redirect(url_for('index'))

    email = confirm_token(token)
    user = services.get_user_by_email(email=current_user.user.email)

    if user.email != email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('inactive'))

    account = services.get_account_by_id(account_id=user.account_id)

    account.is_confirmed = True
    account.confirmed_on = datetime.now()

    db.session.add(account)
    db.session.commit()

    flash('You have confirmed your account. Thanks!', 'success')

    return redirect(url_for('inactive'))


def inactive():
    if not get_flashed_messages():
        return redirect(url_for('index'))

    return render_template(template_name_or_list='mail/inactive.html')


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
    return redirect(url_for('inactive'))
