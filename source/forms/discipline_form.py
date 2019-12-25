from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, BooleanField, HiddenField
from wtforms import validators
from wtforms.validators import NumberRange


class DisciplineForm(Form):
    discipline_id = HiddenField()

    discipline_university = StringField("university: ", [
        validators.DataRequired("Please enter discipline university."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    discipline_faculty = StringField("faculty : ", [
        validators.DataRequired("Please enter discipline faculty."),
        validators.Length(3, 255, "Type should be from 3 to 255 symbols")
    ])

    discipline_name = StringField("name: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    discipline_exam = BooleanField("exam: ")

    discipline_hours_for_semester = IntegerField("hours for semester: ",
                                                 [NumberRange(min=0, max=200, message='number between 0 and 200')])
    submit = SubmitField("Save")

    def strip(self):
        self.discipline_university.data = self.discipline_university.data.strip()
        self.discipline_faculty.data = self.discipline_faculty.data.strip()
        self.discipline_name.data = self.discipline_name.data.strip()

        self.discipline_university.data = self.discipline_university.data.lower()
        self.discipline_faculty.data = self.discipline_faculty.data.lower()
