from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, EmailField, PasswordField, StringField
from wtforms.validators import InputRequired, Length, Optional

class RegisterForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired("Please enter your username"), Length(min=4, max=20)])
  email = EmailField('Email', validators=[InputRequired("Please enter your email address"), Length(min= 1, max=64)])
  password = PasswordField('password', validators=[InputRequired("Please enter your password"), Length(min=8, max=64)])
  confirm_password = PasswordField('confirm_password', validators=[InputRequired("Please confirm your password"), Length(min=8, max=64)])

class LoginForm(FlaskForm):
  email = EmailField('Email', validators=[InputRequired("Please enter your email address"), Length(min=1, max=64)])
  password = PasswordField('password', validators=[InputRequired("Please enter your password"), Length(min=8, max=64)])

class ReviewForm(FlaskForm):
  content= TextAreaField('content', validators=[InputRequired("Please enter your review"), Length(min=1, max=500)])
  id = HiddenField('id', id='gameID', default=-1, validators=[Optional()])