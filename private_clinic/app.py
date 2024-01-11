import os

import cloudinary
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = '1HV98N4L#&UNg?:E;82{Ef@Bftfpl9eC#DtTP~oJ"Pufpi|V)2&}_aqM/g?Pbp2'
app.config['SECURITY_PASSWORD_SALT'] = 'fkslkfsdlkfnsdfnsfd'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:H29012003@localhost/bluefh?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@faithnhope.com'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hieptt.2003@gmail.com'
app.config['MAIL_PASSWORD'] = 'imtj yoby cfvc jeib'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = False

app.config['MAX_PATIENTS_PER_DAY'] = 2
app.config['CURRENT_YEAR'] = 2024

db = SQLAlchemy(app=app)

login = LoginManager(app=app)
login.login_view = 'authentication'

mail = Mail(app=app)

cloudinary.config(
    cloud_name="dtthwldgs",
    api_key="295661242477252",
    api_secret="xKPY2fG-4h1mtZl2_PRvxsSfgtA"
)
