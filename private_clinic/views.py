from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import login_required, current_user, login_user, logout_user

from private_clinic import services
from private_clinic.app import db, login
from private_clinic.decorators import logout_required, check_is_confirmed
from private_clinic.services import send_email
from private_clinic.token import confirm_token, generate_token


def index():
    return render_template(template_name_or_list='index.html')


def about():
    return render_template(template_name_or_list='about.html')


def healthcare_staff():
    return render_template(template_name_or_list='healthcare_staff.html')

def medicine():
    return render_template(template_name_or_list='medicine.html')


@logout_required
def auth():
    return render_template(template_name_or_list='auth.html')


@login_required
@check_is_confirmed
def appointment():
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
        username_signin = request.form.get('username_signin')
        password_signin = request.form.get('password_signin')

        account = services.authenticate(username=username_signin, password=password_signin)

        login_user(account)
        return redirect(url_for('index'))


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
    if (current_user.is_authenticated and current_user.is_confirmed) or not get_flashed_messages():
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
