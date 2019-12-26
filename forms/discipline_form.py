from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField
from wtforms import validators


class DisciplineForm(Form):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])
    teacher_name = StringField("Teacher Name: ", [
        validators.DataRequired("Please enter teacher name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    old_name = HiddenField()

    submit = SubmitField("Save")
