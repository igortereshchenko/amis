from flask_wtf import Form
from wtforms import StringField, SubmitField,HiddenField
from wtforms import validators


class TeacherForm(Form):

    name = StringField("Name: ", [
        validators.DataRequired("Please enter teacher name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    degree = StringField("Degree: ", [
        validators.DataRequired("Please enter teacher degree."),
        validators.Length(0, 255, "Context should be from 0 to 255 symbols")])

    old_name=HiddenField()

    submit = SubmitField("Save")
