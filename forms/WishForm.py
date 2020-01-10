from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField, SelectField
from wtforms import validators

from dao.db import PostgresDb
from dao.orm.model import student, performer, genre, melody

db = PostgresDb()

ch = []
students = list(db.sqlalchemy_session.query(student.id))
studs = []

for i in range(len(students)):
    studs.append(students[i][0])

for i in range(len(students)):
    tuple = students[i][0], students[i][0]
    ch.append(tuple)
print(ch)

ch3 = [(0, 0)]
performers = sorted(list(db.sqlalchemy_session.query(performer.name).distinct()))
pers = []
for i in range(len(performers)):
    pers.append(performers[i][0])

ch1 = [(0, 0)]
genres = sorted(list(db.sqlalchemy_session.query(genre.id).all()))
gens = []
for i in range(len(genres)):
    gens.append(genres[i][0])
for i in range(len(genres)):
    tuple1 = genres[i][0], genres[i][0]
    ch1.append(tuple1)
print(ch1)
ch2 = []
melodies = sorted(list(db.sqlalchemy_session.query(melody.id).all()))
mels = []
for i in range(len(melodies)):
    mels.append(melodies[i][0])
for i in range(len(melodies)):
    tuple2 = melodies[i][0], melodies[i][0]
    ch2.append(tuple2)
print(ch2)
class WishForm(FlaskForm):
    id = HiddenField()

    student_id = SelectField("Оберіть ID студента: ", [
        validators.DataRequired("Це поле є обов'язковим")],
        choices=ch, coerce=int)

    wish_date = DateField("Дата побажання: ", [validators.data_required("Це поле є обов'язковим.")], format='%Y-%m-%d')

    wish_performer = StringField("Оберіть виконавця: ", [validators.any_of(pers, "Перевірте, чи такий виконавець існує")])

    wish_melody = SelectField("Код мелодії: ", None,
                                  choices=ch2, coerce=int)

    wish_genre = SelectField("Код жанру: ", None,
                                  choices=ch1, coerce=int)

    submit = SubmitField("Зберегти")