from flask import render_template


def index():
    return render_template(template_name_or_list='index.html')


def auth():
    return render_template(template_name_or_list='auth.html')
