from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField, SelectField
from wtforms import validators

from dao.db import PostgresDb
from dao.orm.model import performer, genre, album

db = PostgresDb()

ch1 = []
ch2 = []
genres = sorted(list(db.sqlalchemy_session.query(genre.id).distinct()))
gens = []
albums = sorted(list(db.sqlalchemy_session.query(album.id).distinct()))
albs = []
print(albums)
for i in range(len(genres)):
    gens.append(genres[i][0])
for i in range(len(albums)):
    albs.append(albums[i][0])

for i in range(len(genres)):
    tuple1 = genres[i][0], genres[i][0]
    ch1.append(tuple1)

for i in range(len(albums)):
    tuple2 = albums[i][0], albums[i][0]
    ch2.append(tuple2)
print(ch1)
print(ch2)

ch3 = []
performers = sorted(list(db.sqlalchemy_session.query(performer.name).distinct()))
pers = []
for i in range(len(performers)):
    pers.append(performers[i][0])

for i in range(len(performers)):
    tuple3 = performers[i][0], performers[i][0]
    ch3.append(tuple3)

print(ch3)

class MelodyForm(FlaskForm):

    id = HiddenField()

    title = StringField("Назва: ", [
        validators.DataRequired("Введіть назву мелодії."),
        validators.Length(3, 15, "Назва має містити від 3 до 15 символів.")
    ])

    singer = SelectField("Виконавець: ", [
        validators.data_required("Це поле є обов'язковим.")
    ],
                                  choices=ch3)
    release_date = DateField("Дата релізу: ", [validators.data_required("Це поле є обов'язковим.")])

    melody_genre = SelectField("Код жанру: ", [
        validators.data_required("Це поле є обов'язковим.")
    ],
                                  choices=ch1)
    album_id = SelectField("Код альбому: ", [
        validators.data_required("Це поле є обов'язковим.")
    ],
                                  choices=ch2)

    submit = SubmitField("Зберегти")