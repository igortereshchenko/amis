from wtforms import StringField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm
from domain.models import Users
import hashlib

class LoginViewModel(FlaskForm):
    Username = StringField("Username", [validators.DataRequired("Username is required")])
    Password = PasswordField("Password", [validators.DataRequired("Password is required")])

    Submit = SubmitField("Log In")


class SignUpViewModel(FlaskForm):
    Username = StringField("Username", [validators.DataRequired("Username is required")])
    Password = PasswordField("Password", [validators.DataRequired("Password is required"),
                                          validators.equal_to("PasswordRepeat", message="Passwords do not match")])
    PasswordRepeat = PasswordField("Password Repeat", [validators.DataRequired("Password repeat is required")])

    Submit = SubmitField("Sign Up")

    def domain(self):
        return Users(
            Username=self.Username.data,
            Password=hashlib.sha256(self.Password.data.encode()).hexdigest()
        )
