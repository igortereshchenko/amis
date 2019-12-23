from flask_wtf import Form
from wtforms import StringField, SubmitField,HiddenField
from wtforms import validators


class UserForm(Form):

    name = StringField("Name: ", [
        validators.DataRequired("Please enter name.")
    ])

    password = StringField("Password: ", [
        validators.DataRequired("Please enter password.")
    ])


    submit = SubmitField("Login")
