from flask_wtf import FlaskForm
from wtforms import  StringField, validators, SubmitField , IntegerField, DateTimeField, SelectField
from wtforms.validators import NumberRange


from LecturebotDAL.dbcontext import PostgresDb
from LecturebotDAL.models.model import Student
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

class CourseworkForm(FlaskForm):
    initalization_num = IntegerField("Initialization number:", [validators.DataRequired("Введіть ідентифікаційний номер курсової роботи")])
    gradebook_number = SelectField("Gradebook number:",[validators.DataRequired("Введіть номер залікової книги")], choices=ch, coerce=int)
    cwname = StringField("Coursework name:", [validators.DataRequired("Введіть назву роботи")])
    research_direction = StringField("Research direction:", [validators.DataRequired("Введіть напрям досліджень")])
    mark = IntegerField("Mark:")



    submit = SubmitField("Save")