from flask_wtf import FlaskForm
from wtforms import  StringField, validators, SubmitField , IntegerField, DateTimeField, SelectField
from wtforms.validators import NumberRange


from LecturebotDAL.dbcontext import PostgresDb
from LecturebotDAL.models.model import Student, Teacher
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

th = []
perf = sorted(list(db.sqlalchemy_session.query(Teacher.pass_number).distinct()))
per = []
for i in range(len(perf)):
    per.append(perf[i][0])
for i in range(len(perf)):
    tup = perf[i][0], perf[i][0]
    th.append(tup)
print(th)




class Subj_form(FlaskForm):
    pass_num = IntegerField("Subject number:", [validators.DataRequired("Введіть ідентифікаційний номер предмету")])
    sbname = StringField("Name:", [validators.DataRequired("Введіть назву предмета")])
    student_rating = IntegerField("Rating:")
    gradebook_number = SelectField("Gradebook number:",[validators.DataRequired("Введіть номер залікової книги студента ")], choices=ch, coerce=int)
    pass_number = SelectField("Teacher pass number:", [validators.DataRequired("Введіть ідентифікаційний номер викладача")], choices=th, coerce=int)



    submit = SubmitField("Save")