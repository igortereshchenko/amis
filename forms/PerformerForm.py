from flask_wtf import Form, FlaskForm
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators

class PerformerForm(FlaskForm):
    id = HiddenField()

    name = StringField("Performer name: ", [
        validators.DataRequired("Please enter a performer name."),
        validators.Length(3, 15, "Name should be from 3 to 15 symbols")
    ])

    submit = SubmitField("Save")