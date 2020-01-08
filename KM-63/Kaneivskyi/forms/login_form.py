from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, validators


class LoginForm(Form):
    user_name = StringField("name: ", [
        validators.Length(3, 20, "Name should be from 3 to 20 symbols"),
        validators.DataRequired("Please enter your name.")
    ])
    user_password = PasswordField("password: ", [
        validators.DataRequired("Please enter your password."),
    ])

    submit = SubmitField("sing in")