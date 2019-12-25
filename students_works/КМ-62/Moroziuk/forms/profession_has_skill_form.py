from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, SelectField


class ProfessionSkillForm(FlaskForm):
   id = HiddenField("Id")

   skill_id = SelectField("skill: ", choices=[], coerce=int)#,[validators.DataRequired(),])

   profession = SelectField("profession: ", choices=[], coerce=int)#,[validators.DataRequired(),])

   submit = SubmitField("Save")