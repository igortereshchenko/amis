from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, validators, SubmitField


class SkillForm(FlaskForm):
   id = HiddenField("Id")

   name = StringField("Skill name: ",[
                                    validators.DataRequired("Please enter skill name."),
   ])

   submit = SubmitField("Save")