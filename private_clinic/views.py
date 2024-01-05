from flask import render_template, request, redirect, url_for, session, jsonify
from private_clinic import services


def index():
    return render_template(template_name_or_list='index.html')


def about():
    return render_template(template_name_or_list='about.html')


def healthcare_staff():
    return render_template(template_name_or_list='healthcare_staff.html')

def auth():
    return render_template(template_name_or_list='auth.html')


def appointment():
    return render_template(template_name_or_list='appointment.html')

def profile_settings():
    return render_template(template_name_or_list='profile_settings.html')

def recovery_password():
    return render_template(template_name_or_list='recovery_password.html')

def signup():
    if request.method.__eq__('POST'):
        username = request.form.get('username_signup')
        password = request.form.get('password_signup')
        confirm_password = request.form.get('confirm_password_signup')

        try:
            if password.strip().__eq__(confirm_password.strip()):
                services.create_account(username=username, password=password)
        except Exception as ex:
            pass

        first_name = request.form.get('firstname_signup')
        last_name = request.form.get('lastname_signup')
        email = request.form.get('email_signup')
        phone = request.form.get('phone_signup')
