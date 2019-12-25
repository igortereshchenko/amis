from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField
from datetime import date
from wtforms import validators


class ApplyForm(Form):
    user_id = HiddenField()

    user_login = StringField("login: ", [
        validators.DataRequired("Please enter user`s login."),
        validators.Length(3, 255, "Text should be from 3 to 255 symbols")
    ])

    user_pass = StringField("password: ", [
        validators.DataRequired("Please enter teacher`s faculty."),
        validators.Length(2, 255, "Text should be from 2 to 255 symbols")
    ])

    submit = SubmitField("Save")
