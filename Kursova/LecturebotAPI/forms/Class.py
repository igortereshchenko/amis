from flask_wtf import FlaskForm
from wtforms import  StringField, validators, SubmitField , IntegerField, DateTimeField, SelectField
from wtforms.validators import NumberRange


from LecturebotDAL.dbcontext import PostgresDb
from LecturebotDAL.models.model import Student, Teacher, Subject
db = PostgresDb()

ch = []
performers = sorted(list(db.sqlalchemy_session.query(Student.gradebook_number).distinct()))
pers = []
for i in range(len(performers)):
    pers.append(performers[i][0])
for i in range(len(performers)):
    tuple = performers[i][0], performers[i][0]
    ch.append(tuple)
print(ch)


class Classform(FlaskForm):

    gradebook_number = SelectField("Gradebook number:",[validators.DataRequired("Введіть номер залікової книги студента ")], choices=ch, coerce=int)
    submit = SubmitField("Start")

