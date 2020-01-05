from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class SearchForm(FlaskForm):
   search = StringField("search: ",[
        validators.DataRequired("Please enter"),
   ])

   submit = SubmitField("Save")