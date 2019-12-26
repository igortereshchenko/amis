from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class EditStoreForm(Form):
    store_id = HiddenField("id:")

    store_name = StringField("Name: ", [
        validators.DataRequired("Please enter your name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    store_link = StringField("link: ", [
        validators.DataRequired("Please enter your link."),
        validators.Length(0, 50, "Link should be from 3 to 20 symbols")
    ])




    submit = SubmitField("Save")