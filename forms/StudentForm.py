from flask_wtf import FlaskForm
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators

class StudentForm(FlaskForm):
    id = HiddenField()

    faculty = StringField("Faculty: ", [
        validators.DataRequired("Please enter a faculty."),
        validators.Length(3, 15, "Faculty should be from 3 to 20 symbols")
    ])

    group = StringField("Group: ", [
        validators.DataRequired("Please enter your group."),
        validators.regexp('[A-Z][A-Z]-[0-9][0-9]')
    ])

    name = StringField("Name: ", [
        validators.DataRequired("Please enter your name."),
        validators.Length(3, 15, "Name should be from 3 to 15 symbols")
    ])

    surname = StringField("Surname: ", [
        validators.DataRequired("Please enter surname."),
        validators.Length(3, 15, "Surname should be from 3 to 15 symbols")
    ])

    username = StringField("Username: ", [
        validators.DataRequired("Please enter username."),
        validators.Length(3, 36, "Username should be from 3 to 36 symbols"),
        validators.regexp('@([A-Z]|[a-z]|_)*')
    ])

    submit = SubmitField("Save")