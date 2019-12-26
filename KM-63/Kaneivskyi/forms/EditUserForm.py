from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class EditUserForm(Form):
    user_name = HiddenField("id:")

    user_password = StringField("password: ", [
        validators.DataRequired("Please enter your password."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])


    submit = SubmitField("Save")