from flask_wtf import FlaskForm
from wtforms import  validators, SubmitField, SelectField, StringField, IntegerField


class HouseForm(FlaskForm):
    build_num = IntegerField("Building number:",[validators.number_range(1,16,"Value should be from 1 to 16")])
    adress = StringField("Adress:")
    floors = IntegerField("Floor_num:")
    years = IntegerField("Year of build:",[validators.number_range(1980,None,"Value should be from 1980")])



    submit = SubmitField("Save")