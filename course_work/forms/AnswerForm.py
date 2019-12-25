from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField

from model import model
from model.university_faculties import university_faculties


# Working table
class AnswerForm(FlaskForm):
    Questions = SelectField("Question", validators=[validators.DataRequired()])
    Answer_for_question = StringField("Answer", [validators.DataRequired("Answer is required")])
    Student_answer = SelectField("Student", validators=[validators.DataRequired()])
    User_faculty = SelectField("Faculty", validators=[validators.DataRequired()], choices=university_faculties)

    Submit = SubmitField("Save answer & send email")

    def model(self):
        return model.AnswerTable(
            QuestionIdFk=self.Questions.data,
            Answer_for_question=self.Answer_for_question.data,
            StudentIdFk=self.Student_answer.data,
            User_faculty=self.User_faculty.data
        )

# class AnswerForm(FlaskForm):
#     Answer_for_question = StringField("answer_for_question", [validators.DataRequired("Answer is required")])
#     Student_answer = SelectField("student_answer", validators=[validators.DataRequired()])
#     Questionnaire_title = SelectField("questionnaire_title", validators=[validators.DataRequired()])
#
#     Submit = SubmitField("Save")
#
#     def model(self):
#         return model.AnswerTable(
#             Answer_for_question=self.Answer_for_question.data,
#             StudentIdFk=self.Student_answer.data,
#             QuestionnaireIdFks=self.Questionnaire.data
#         )
