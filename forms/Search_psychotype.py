from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators

from dao import db
from dao.db import PostgresDb
from dao.orm.model import student

db = PostgresDb()

faculties = list(db.sqlalchemy_session.query(student.faculty).all())

class SearchPsychForm(FlaskForm):
    id = HiddenField()

    faculty = StringField("Введіть факультет для виявлення психотипу студентів: ", [
        validators.data_required("Це поле є обов'язковим"),
        validators.any_of(faculties)])

    submit = SubmitField("Шукати")