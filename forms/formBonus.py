from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators


class BonusForm(FlaskForm):


    name = StringField("name: ", [
        validators.DataRequired("Please enter your function.")

    ])

    value = StringField("value: ", [
        validators.DataRequired("Please enter your function type.")

    ])


    submit = SubmitField("Save")
