from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators


class EditUser(FlaskForm):
    name = StringField("name: ", [
        validators.DataRequired("Please enter your name.")

    ])

    surname = StringField("surname: ", [
        validators.DataRequired("Please enter your surname.")

    ])

    birthday = DateField("birthday: ", [
        validators.DataRequired("Please enter your birthday.")

    ])

    submit = SubmitField("Save")


    def validate_on_submit(self):
        result = super(EditUser, self).validate()
        print(self.birthday.data.year)
        if self.birthday.data.year < 1900:
            return False
        else:
            return result
