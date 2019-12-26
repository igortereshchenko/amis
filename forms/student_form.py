from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms import validators


class StudentForm(Form):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter student name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    group = IntegerField("Group: ", [
        validators.DataRequired("Please enter student Group.")])

    old_name = HiddenField()

    old_group = HiddenField()
    submit = SubmitField("Save")
