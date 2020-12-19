import os
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Please log in to access this page'
bootstrap = Bootstrap(app)

from app import routes, models, errors


