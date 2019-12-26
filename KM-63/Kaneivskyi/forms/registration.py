from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, validators


class RegistrationForm(Form):
    user_name = StringField("name: ", [
        validators.Length(3, 20, "Name should be from 3 to 20 symbols"),
        validators.DataRequired("Please enter your name.")
    ])
    user_password = PasswordField("password: ", [
        validators.DataRequired("Please enter your name."),
    ])
    user_confirm_password = PasswordField("confirm password: ", [
        validators.DataRequired("Please enter your name."),
        validators.EqualTo('user_password', message='Passwords must match')
    ])

    submit = SubmitField("sign up")