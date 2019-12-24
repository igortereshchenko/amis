from wtforms import StringField, DateTimeField, IntegerField, SubmitField, validators
from flask_wtf import FlaskForm
from domain import models
from wtforms.validators import DataRequired, Length, Email, NumberRange



class ClientsViewModel(FlaskForm):

    Client_name = StringField("Client_name: ", [validators.DataRequired("Please enter your Name.")])
    Age = IntegerField("Age: ", [validators.NumberRange(min=1),validators.DataRequired("Age can not be < 0.")])
    Money = IntegerField("Money: ",  [validators.NumberRange(min=1),validators.DataRequired("Money can not be < 0.")])
    Contact = IntegerField("Contact: ", [validators.DataRequired("Please enter your Contact.")])
    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Clients(
            Client_name=self.Client_name.data,
            Age=self.Age.data,
            Money=self.Money.data,
            Contact=self.Contact.data,
            CreatedOn=self.CreatedOn.data
        )