from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators
from wtforms.validators import NumberRange, Required, DataRequired


class EditEvent(FlaskForm):
    name = StringField("name: ", [
        validators.DataRequired("Please enter your name.")

    ])

    user_id_fk = IntegerField("user_id_fk: ",
        validators=[NumberRange(min=1, message=">1"), DataRequired("Please enter your user_id.")]

    )

    category = StringField("category: ", [
        validators.DataRequired("Please enter your category.")

    ])

    city = StringField("city: ", [
        validators.DataRequired("Please enter your city.")

    ])

    dates = DateField("date: ", [
        validators.DataRequired("Please enter your date.")

    ])

    price = IntegerField("price: ",
                         validators=[NumberRange(min=1, message=">1"), DataRequired("Please enter your price.")]

                         )

    hashtag = StringField("hashtag: ",[
                          validators.DataRequired("Please enter your hashtag.")])

    adress = StringField("adress: ", [
        validators.DataRequired("Please enter your adress.")

    ])
    count_of_people = IntegerField("count of people: ",
                         validators=[NumberRange(min=1, message=">1"), DataRequired("Please enter your count of people.")]
                         )
    submit = SubmitField("Save")

    def validate_on_submit(self):
        result = super(EditEvent, self).validate()
        print(self.dates.data.year)
        if self.dates.data.year < 1900:
            return False
        else:
            return result

