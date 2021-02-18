from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if app.config['ENV'] == 'testing':
    app.config.from_object('src.accountment.config.TestingConfig')
else:
    app.config.from_object('src.accountment.config.DevelopmentConfig')

db = SQLAlchemy(app)

from .routes import employees, customers, jobs, assign, errors
