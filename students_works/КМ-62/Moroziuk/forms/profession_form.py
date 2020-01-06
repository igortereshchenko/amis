from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, validators, SubmitField
from wtforms.fields.html5 import IntegerField


class ProfessionForm(FlaskForm):
   id = HiddenField("Id")

   name = StringField("Profession name: ",[
        validators.DataRequired("Please enter name."),
   ])

   minimal_work_expirience = IntegerField("Minimal work expirience: ",
        [validators.DataRequired("Minimal work expirience required"), validators.NumberRange(min=0, max=100)]
    )

   minimal_education = StringField("Minimal education: ", [
       validators.DataRequired("Please enter your birthday."),
       validators.length(4, 60, "Pleas select between 4 to 60")
   ])

   category = StringField("Category: ",[
       validators.DataRequired("Please enter category."),
       validators.length(10, 100, "Pleas select between 10 to 100")
    ])

   submit = SubmitField("Save")