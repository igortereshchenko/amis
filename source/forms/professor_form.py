from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField
from datetime import date
from wtforms import validators


class ProfessorForm(Form):
    professor_id = HiddenField()

    professor_name = StringField("name: ", [
        validators.DataRequired("Please enter professor name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    professor_surname = StringField("surname: ", [
        validators.DataRequired("Please enter professor surname."),
        validators.Length(3, 255, "Type should be from 3 to 255 symbols")
    ])

    professor_university = StringField("university: ", [
        validators.DataRequired("Please enter professor university."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    professor_department = StringField("department : ", [
        validators.DataRequired("Please enter professor department ."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    professor_degree = StringField("Degree: ", [
        validators.Length(0, 255, "Context should be from 0 to 255 symbols")])

    professor_date_enrollment = DateField("date enrollment: ", [
        validators.DataRequired("Please enter professor date enrollment.")], format='%d-%b-%y', default=date.today())

    professor_date_expelled = DateField("date expelled: ", [validators.Optional()], format='%d-%b-%y')

    submit = SubmitField("Save")

    def strip(self):
        self.professor_name.data = self.professor_name.data.strip()
        self.professor_surname.data = self.professor_surname.data.strip()
        self.professor_university.data = self.professor_university.data.strip()
        self.professor_department.data = self.professor_department.data.strip()
        self.professor_degree.data = self.professor_degree.data.strip()

        self.professor_university.data = self.professor_university.data.lower()
        self.professor_department.data = self.professor_department.data.lower()
