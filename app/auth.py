from app import app, db
from .models import Users
from flask_login import LoginManager
from flask import redirect, url_for

login_manager = LoginManager()
login_manager.init_app(app)


# load user from database
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


# if user is not logged in, redirect to login page
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
