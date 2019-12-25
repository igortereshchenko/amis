from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

from forms.AnswerForm import AnswerForm
from forms.QuestionForm import QuestionForm
from forms.QuestionnaireForm import QuestionnaireForm
from forms.UniversityUsersForm import UniversityUserForm

db = SQLAlchemy()


class UniversityUsersTable(db.Model, UserMixin):
    __tablename__ = 'users_table'

    UserFullName = db.Column("user_fullname", db.String, nullable=False)
    User_email = db.Column("user_email", db.String, primary_key=True)
    User_password = db.Column("user_password", db.String, nullable=False)
    User_faculty = db.Column("user_faculty", db.String, nullable=False)

    def get_id(self):
        return self.User_email

    def filled_form(self):
        return UniversityUserForm(
            UserFullName=self.UserFullName,
            User_email=self.User_email,
            User_password=self.User_password,
            User_faculty=self.User_faculty
        )

    def map_to_form(self, form):
        self.UserFullName = form.UserFullName.data
        self.User_email = form.User_email.data
        self.User_password = form.User_password.data
        self.User_faculty = form.User_faculty.data


class QuestionsTable(db.Model):
    __tablename__ = 'questions_table'

    Question_id = db.Column("question_id", db.Integer, primary_key=True)
    Questions = db.Column("questions", db.String, nullable=False)
    Type_question = db.Column("type_question", db.String, nullable=False)

    def filled_form(self):
        return QuestionForm(
            Questions=self.Questions,
            Type_question=self.Type_question)

    def map_to_form(self, form):
        self.Questions = form.Questions.data,
        self.Type_question = form.Type_question.data


class QuestionnaireTable(db.Model):
    __tablename__ = 'questionnaire_table'
    Questionnaire_id = db.Column("questionnaire_id", db.Integer, primary_key=True)
    User_faculty = db.Column("user_faculty", db.String, nullable=False)

    QuestionIdFk = db.Column("question_id_fk", db.Integer, db.ForeignKey("questions_table.question_id"),
                             primary_key=True)
    Question = db.relationship("QuestionsTable", backref=backref('children2', cascade='all,delete'),
                               passive_deletes=True)

    def filled_form(self):
        return QuestionnaireForm(
            Questionnaire_id=self.Questionnaire_id,
            User_faculty=self.User_faculty,
            Question=self.QuestionIdFk
        )

    def map_to_form(self, form):
        self.Questionnaire_id = form.Questionnaire_id.data
        self.QuestionIdFk = form.Questions.data
        self.User_faculty = form.User_faculty.data


class AnswerTable(db.Model):
    __tablename__ = 'answer_table'

    Answer_id = db.Column("answer_id", db.Integer, primary_key=True)
    Answer_for_question = db.Column("answer_for_question", db.String, nullable=False)
    User_faculty = db.Column("user_faculty", db.String, nullable=False)

    StudentIdFk = db.Column("student_id_fk", db.String, db.ForeignKey("users_table.user_email"))
    Student_answer = db.relationship("UniversityUsersTable", backref=backref('children3', cascade='all,delete'),
                                     passive_deletes=True)

    QuestionIdFk = db.Column("question_id_fk", db.Integer, db.ForeignKey("questions_table.question_id"))
    Question = db.relationship("QuestionsTable", backref=backref('children4', cascade='all,delete'),
                               passive_deletes=True)

    def filled_form(self):
        return AnswerForm(
            Question=self.QuestionIdFk,
            Answer_for_question=self.Answer_for_question,
            Student_answer=self.StudentIdFk,
            User_faculty=self.User_faculty
        )

    def map_to_form(self, form):
        self.Answer_for_question = form.Answer_for_question.data,
        self.StudentIdFk = form.Student_answer.data,
        self.QuestionIdFk = form.Questions.data,
        self.User_faculty = form.User_faculty.data
