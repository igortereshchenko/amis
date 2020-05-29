from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms import validators
from dao.db import PostgresDb
from dao.orm.entities import *
from datetime import date

db = PostgresDb()

class SceduleForm(Form):
    STATE_CHOICES = [('8:30-10:05', '8:30-10:05'), ('10:20-12:00', '10:20-12:00'), ('12:15-13:55', '12:15-13:55'), ('14:15-15:55', '14:15-15:55')]
    STATE_CH =[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')]
    group_id_fk = IntegerField("group id: ", [
        validators.DataRequired("Please enter group`s id.")
    ])

    teach_id_fk = IntegerField("teacher`s id: ", [
        validators.DataRequired("Please enter teacher`s id.")
    ])

    subj_name_fk = StringField("subject name: ", [
        validators.DataRequired("Please enter subject name."),
        validators.Length(3, 255, "Text should be from 3 to 255 symbols")
    ])

    times = SelectField(choices = STATE_CHOICES)

    days = SelectField(choices = STATE_CH)

    auditorium = StringField("auditorium: ", [
        validators.DataRequired("Please enter auditorium.")
    ])
    submit = SubmitField("Save")
