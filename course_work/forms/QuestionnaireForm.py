from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, SelectField, IntegerField

from model import model
from model.university_faculties import university_faculties


# Working table
class QuestionnaireForm(FlaskForm):
    Questionnaire_id = IntegerField("Questionnaire ID", validators=[validators.NumberRange(min=1),
                                                                    validators.DataRequired(
                                                                        "Id can't be 0 and must be number")])
    Questions = SelectField("Question", validators=[validators.DataRequired()])
    User_faculty = SelectField("Faculty", [validators.DataRequired("Faculty is required")],
                               choices=university_faculties)

    Submit = SubmitField("Save")

    def model(self):
        return model.QuestionnaireTable(
            Questionnaire_id=self.Questionnaire_id.data,
            QuestionIdFk=self.Questions.data,
            User_faculty=self.User_faculty.data
        )