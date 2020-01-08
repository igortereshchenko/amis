from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class CharacteristicForm(Form):

    charac_name = StringField("Name: ", [
        validators.DataRequired("Please enter your name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])
    charac_description = StringField("Description: ", [
        validators.DataRequired("Please enter your description."),
        validators.Length(3, 20, "Description should be from 3 to 20 symbols")
    ])
    goods_fk = IntegerField("goods_fk: ", [validators.DataRequired("Please enter your description."),
                                           validators.NumberRange(min=0, max=1000, message="Must be between from 0 to 1000")])

    submit = SubmitField("Save")