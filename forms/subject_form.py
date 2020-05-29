from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, BooleanField, HiddenField
from datetime import date
from wtforms import validators


class SubjectForm(Form):
    old_name = HiddenField()

    subject_name = StringField("name: ", [
        validators.DataRequired("Please enter subject`s name."),
        validators.Length(3, 255, "Text should be from 3 to 255 symbols")
    ])


    subject_hours = IntegerField("Hours per week: ")

    submit = SubmitField("Save")
