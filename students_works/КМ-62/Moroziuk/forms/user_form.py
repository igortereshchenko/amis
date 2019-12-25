from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, validators, SubmitField, DateTimeField


class UserForm(FlaskForm):
   id = HiddenField("Id")

   first_name = StringField("First name: ",[
        validators.DataRequired("Please enter your name."),
   ])

   second_name = StringField("Second name: ", [
       validators.DataRequired("Please enter your name."),
   ])

   birthday = DateTimeField("Birthday: ", [
       validators.DataRequired("Please enter your birthday.")])

   city = StringField("City: ",[
       validators.DataRequired("Please enter your city.")
    ])

   submit = SubmitField("Save")