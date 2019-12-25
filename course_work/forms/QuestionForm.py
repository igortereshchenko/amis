from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField

from model import model
from model.question_types import question_types


class QuestionForm(FlaskForm):
    Questions = StringField("Question", validators=[validators.DataRequired("Question can't be empty")])
    Type_question = SelectField("Type of question", [validators.DataRequired("Type is required")], choices=question_types)

    Submit = SubmitField("Save")

    def model(self):
        return model.QuestionsTable(
            Questions=self.Questions.data,
            Type_question=self.Type_question.data
        )
