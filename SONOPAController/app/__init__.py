__author__ = 'hasier'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

principals = Principal(app)

app.config['UPDATE-SOCIAL-NETWORK'] = True
app.config['FAKE-SENSORS'] = False


from app import views, models
