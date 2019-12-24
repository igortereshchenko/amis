from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators


class CreateBonus(FlaskForm):
    event_id = IntegerField("event id: ", [validators.DataRequired("Please enter your function.")])

    name = StringField("name: ", [
        validators.DataRequired("Please enter your function.")

    ])

    value = StringField("value: ", [
        validators.DataRequired("Please enter your function type.")

    ])


    submit = SubmitField("Save")
