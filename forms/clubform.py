from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators
from wtforms.validators import NumberRange, Required, DataRequired


class editClub(FlaskForm):
    adress = StringField("adress: ", [
        validators.DataRequired("Please enter your name.")

    ])
    name = StringField("name: ", [
        validators.DataRequired("Please enter your name.")

    ])

    price = IntegerField("price: ",
                         validators=[NumberRange(min=0, message=">1"), DataRequired("Please enter your price.")]
                         )

    year = StringField("year: ",[
                          validators.DataRequired("Please enter your hashtag.")])



    submit = SubmitField("Save")

    def validate_on_submit(self):
        result = super(editClub, self).validate()

        if self.name.data == "k1" or self.name.data == "k2":
            return result
        else:
            return False



