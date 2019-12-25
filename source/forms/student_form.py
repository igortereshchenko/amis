from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField
from wtforms import validators
from datetime import date


class StudentForm(Form):
    student_id = HiddenField()

    student_login = StringField("login: ", [
        validators.DataRequired("Please enter student login."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    student_password = StringField("password: ", [
        validators.DataRequired("Please enter student password."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    student_name = StringField("name: ", [
        validators.DataRequired("Please enter student name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    student_surname = StringField("surname: ", [
        validators.DataRequired("Please enter student surname."),
        validators.Length(3, 255, "Type should be from 3 to 255 symbols")
    ])

    student_group = StringField("Group: ", [
        validators.DataRequired("Please enter student Group."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    student_university = StringField("university: ", [
        validators.DataRequired("Please enter student university."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    student_faculty = StringField("faculty: ", [
        validators.DataRequired("Please enter student faculty."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    student_date_enrollment = DateField("date enrollment: ", [
        validators.DataRequired("Please enter student date enrollment.")], format='%d-%b-%y', default=date.today())

    student_date_expelled = DateField("date expelled: ", [validators.Optional()], format='%d-%b-%y')

    submit = SubmitField("Save")

    def strip(self):
        self.student_login.data = self.student_login.data.strip()
        self.student_password.data = self.student_password.data.strip()
        self.student_name.data = self.student_name.data.strip()
        self.student_surname.data = self.student_surname.data.strip()
        self.student_group.data = self.student_group.data.strip()
        self.student_university.data = self.student_university.data.strip()
        self.student_faculty.data = self.student_faculty.data.strip()

        self.student_group.data = self.student_group.data.lower()
        self.student_university.data = self.student_university.data.lower()
        self.student_faculty.data = self.student_faculty.data.lower()

