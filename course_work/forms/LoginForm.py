from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, StringField, PasswordField, SelectField

from model.university_faculties import university_faculties


class LoginForm(FlaskForm):
    User_email = StringField("Enter your email", [validators.DataRequired("Enter user's email")])
    User_password = PasswordField("Enter your password", [validators.DataRequired("Enter user's password")])

    Submit = SubmitField("Log in")
