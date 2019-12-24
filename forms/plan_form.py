from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators
from wtforms.validators import NumberRange, DataRequired


class CreatePlan(FlaskForm):
    event_id = IntegerField("event_id: ", validators=[NumberRange(min=1, message=">1"),DataRequired("Please enter your id.")])

    newSkill = StringField("newSkill: ", [
        validators.DataRequired("Please enter your newSkill.")

    ])

    description = StringField("description: ", [
        validators.DataRequired("Please enter your description.")

    ])

    company = StringField("company: ", [
        validators.DataRequired("Please enter your company.")

    ])

    category = StringField("category: ", [
        validators.DataRequired("Please enter your category.")

    ])

    submit = SubmitField("Save")


class EditPlan(FlaskForm):
    newSkill = StringField("newSkill: ", [
        validators.DataRequired("Please enter your newSkill.")

    ])

    description = StringField("description: ", [
        validators.DataRequired("Please enter your description.")

    ])

    company = StringField("company: ", [
        validators.DataRequired("Please enter your company.")

    ])

    category = StringField("category: ", [
        validators.DataRequired("Please enter your category.")

    ])

    submit = SubmitField("Save")
