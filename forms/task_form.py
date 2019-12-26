from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, HiddenField, TimeField
from wtforms import validators


class TaskFrom(Form):

    name = StringField("Name: ", [
        validators.DataRequired("Please enter student name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    discipline_name = StringField("Discipline: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    value = IntegerField("Value: ", [
        validators.DataRequired("Please enter discipline name.")
    ])
    deadline = TimeField("Deadline: ", [
        validators.DataRequired("Please enter discipline name.")
    ], format= '%H:%M:%S')


    old_name = HiddenField()

    submit = SubmitField("Save")
