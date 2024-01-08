from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from private_clinic.models import AccountRoleEnum


def employee_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role == AccountRoleEnum.PATIENT:
            flash('Please log in to your staff account to access this website', 'warning')
            return redirect(url_for('notification'))
        return func(*args, **kwargs)

    return decorated_function


def employee_logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role != AccountRoleEnum.PATIENT:
            flash('You are already authenticated.', 'info')
            return redirect(url_for('notification'))
        return func(*args, **kwargs)

    return decorated_function


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already authenticated.', 'info')
            return redirect(url_for('notification'))
        return func(*args, **kwargs)

    return decorated_function


def check_is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('notification'))
        return func(*args, **kwargs)

    return decorated_function


def check_role(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.role != role:
                flash('Please log in to your account with the correct role', 'warning')
                return redirect(url_for('notification'))
            return func(*args, **kwargs)

        return decorated_function

    return decorator
