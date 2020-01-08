from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class UserForm(Form):

    user_name = StringField("Name: ", [
        validators.DataRequired("Please enter your password."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    user_password = PasswordField("Name: ", [
        validators.DataRequired("Please enter your password."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    submit = SubmitField("Save")
