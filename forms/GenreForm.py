from flask_wtf import Form, FlaskForm
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators

class GenreForm(FlaskForm):

    id = HiddenField()

    genre_name = StringField("Genre name: ", [
        validators.DataRequired("Please enter a genre name."),
        validators.Length(3, 15, "Value should be from 3 to 15 symbols")
    ])

    psychotype = StringField("Psychotype: ", [
        validators.DataRequired("Please enter psychotype."),
        validators.Length(3, 15, "Value should be from 3 to 20 symbols")
    ])

    submit = SubmitField("Save")