from flask_wtf import FlaskForm
from wtforms import  StringField, validators, SubmitField , IntegerField, DateTimeField
from wtforms.validators import NumberRange
from wtforms.fields.html5 import DateField

class Studform(FlaskForm):

    gradebook_number = IntegerField("Gradebook number:", [validators.DataRequired("Введіть номер залікової книги")])
    full_name = StringField("Student name: ", [
                                    validators.DataRequired("Введіть повне ім'я студента")
    ])
    stgroup = StringField("Group:")
    year_of_receipt = DateField('Year of receipt:',[validators.DataRequired("Введіть номер залікової книги")], format='%Y-%m-%d')
    submit = SubmitField("Save")

