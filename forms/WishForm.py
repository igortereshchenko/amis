from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField, SelectField
from wtforms import validators

from dao.db import PostgresDb

class WishForm(FlaskForm):
    id = HiddenField()
    student_id = SelectField()
    wish_date = DateField()
    nickname = StringField()
    wish_performer = StringField()
    wish_melody = SelectField()
    wish_genre = SelectField()