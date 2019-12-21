from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField, SelectField
from wtforms import validators

from dao import db
from dao.db import PostgresDb
from dao.orm.model import student

db = PostgresDb()

ch = []
faculties = list(db.sqlalchemy_session.query(student.faculty).distinct())
facs = []
for i in range(len(faculties)):
    facs.append(faculties[i][0])
for i in range(len(faculties)):
    # values.append(faculties[i][0])
    # labels.append(faculties[i][0])
    tuple = faculties[i][0], faculties[i][0]
    ch.append(tuple)
print(ch)

class SearchPsychForm(FlaskForm):
    id = HiddenField()

    # faculty = StringField("Введіть факультет для виявлення психотипу студентів: ", [
    #     validators.data_required("Це поле є обов'язковим"),
    #     validators.any_of(facs)])

    fac = SelectField("Оберіть факультет для виявлення психотипу студентів: ", [
        validators.DataRequired("Це поле є обов'язковим")], choices=ch)

    submit = SubmitField("Шукати")