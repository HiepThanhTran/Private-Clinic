from flask import render_template, request, redirect, url_for, session, jsonify


def index():
    return render_template(template_name_or_list='index.html')


def auth():
    return render_template(template_name_or_list='auth.html')


def signup():
    if request.method.__eq__('POST'):
        username = request.form.get('username_signup')
        password = request.form.get('password_signup')
        confirm_password = request.form.get('confirm_password_signup')



        first_name = request.form.get('firstname_signup')
        last_name = request.form.get('lastname_signup')
        email = request.form.get('email_signup')
        phone = request.form.get('phone_signup')


def appointment():
    return render_template(template_name_or_list='appointment.html')
