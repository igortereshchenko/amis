from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators


class CreateQuery(FlaskForm):

    city = StringField("City: ", [validators.DataRequired("Please enter your city.")])

    date = DateField("Date: ", [
        validators.DataRequired("Please enter your date.")

    ])

    name_of_event = StringField("Category: ", [
        validators.DataRequired("Please enter your event.")

    ])

    submit = SubmitField("Search")

    def validate_on_submit(self):
        result = super(CreateQuery, self).validate()
        print(self.date.data.year)
        if self.date.data.year < 1900:
            return False
        else:
            return result
