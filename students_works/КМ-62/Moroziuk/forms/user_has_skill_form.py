from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, SelectField


class UserSkillForm(FlaskForm):
   id = HiddenField("Id")

   skill_id = SelectField("skill: ", choices=[], coerce=int)#,[validators.DataRequired(),])

   user_id = SelectField("user: ", choices=[], coerce=int)#,[validators.DataRequired(),])

   submit = SubmitField("Save")