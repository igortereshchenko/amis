from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField, SelectField
from wtforms import validators

from dao.db import PostgresDb
from dao.orm.model import performer

db = PostgresDb()

ch = []
performers = sorted(list(db.sqlalchemy_session.query(performer.id).distinct()))
pers = []
for i in range(len(performers)):
    pers.append(performers[i][0])
for i in range(len(performers)):
    # values.append(faculties[i][0])
    # labels.append(faculties[i][0])
    tuple = performers[i][0], performers[i][0]
    ch.append(tuple)
print(ch)


class AlbumForm(FlaskForm):

    id = HiddenField()

    album_name = StringField("Назва: ", [
        validators.DataRequired("Введіть назву альбому."),
        validators.Length(3, 15, "Назва має містити від 3 до 15 символів.")
    ])

    album_performer = SelectField("Код виконавця: ", [
        validators.data_required("Це поле є обов'язковим.")
    ],
                                  choices=ch, coerce=int)

    submit = SubmitField("Зберегти")