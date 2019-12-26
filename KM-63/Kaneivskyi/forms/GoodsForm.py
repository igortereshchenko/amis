from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class GoodsForm(Form):
    good_id = IntegerField("id: ", [validators.DataRequired("Please enter your description."),
                                           validators.NumberRange(min=0, max=100, message="Must be between from 0 to 100")])

    good_name = StringField("Name: ", [
        validators.DataRequired("Please enter your name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    good_model = StringField("Model: ", [
        validators.DataRequired("Please enter your model."),
        validators.Length(0, 20, "Model should be from 3 to 20 symbols")
    ])

    price = IntegerField("Price: ", [validators.DataRequired("Please enter your price."),
                                           validators.NumberRange(min=0, max=1000, message="Must be between from 0 to 1000")])

    stores = IntegerField("Stores: ", [validators.DataRequired("Please enter your stores."),
                                       validators.NumberRange(min=0, max=1000, message="Must be between from 0 to 1000")
                                       ])

    users = StringField("User: ", [
        validators.DataRequired("Please enter your user."),
        validators.Length(0, 20, "Model should be from 3 to 20 symbols")])




    submit = SubmitField("Save")