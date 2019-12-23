from wtforms import StringField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm
from domain.models import Users


class LoginViewModel(FlaskForm):
    Login = StringField("Username", [validators.DataRequired("Login is required")])
    Password = PasswordField("Password", [validators.DataRequired("Password is required")])

    Submit = SubmitField("Log In")


    def domain(self):
        return Users(
            Login=self.Login.data,
            Password=self.Password.data
        )