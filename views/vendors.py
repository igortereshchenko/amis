from wtforms import StringField, DateTimeField, SubmitField, validators, SelectField, IntegerField
from flask_wtf import FlaskForm
from domain import models
from domain.layout import country_type



class VendorsViewModel(FlaskForm):
    vendor_name = StringField("Name: ", [validators.DataRequired("Please enter vendors Name.")])
    vendor_address = StringField("Address: ",[validators.DataRequired("Please enter vendors Address.")])
    balance = IntegerField("Balance: ",[validators.NumberRange(min=1),validators.DataRequired("Can not be 0.")])
    vendor_country = SelectField("Country: ", [validators.DataRequired("Country is required.")], choices=country_type)
    Clothe = SelectField("Clothe ", validators=[validators.DataRequired()])
    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")


    def domain(self):
        return models.Vendors(
            vendor_name=self.vendor_name.data,
            vendor_address=self.vendor_address.data,
            balance=self.balance.data,
            CreatedOn=self.CreatedOn.data,
            vendor_country=self.vendor_country.data,
            clothe_idIdFk=self.Clothe.data
        )