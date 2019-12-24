from wtforms import StringField, DateTimeField, SubmitField, validators, SelectField, IntegerField
from flask_wtf import FlaskForm
from domain import models
from wtforms.validators import DataRequired, Length, Email, NumberRange
from datetime import date, datetime





class VendorsViewModel(FlaskForm):
    Vendor_name = StringField("Vendor_name: ", [validators.DataRequired("Please enter  Vendor_name.")])
    City = StringField('City', [DataRequired("Enter City"), Length(1,9,"City should be in range [1;9] ")])
    Rating =  IntegerField("Rating", [DataRequired("Rating must be >0"), NumberRange(min=1,)])
    Year = IntegerField("Year: ", [validators.DataRequired("Please enter  Year.")])
    Product = SelectField("Product ", validators=[validators.DataRequired()])
    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Vendors(
            Vendor_name=self.Vendor_name.data,
            City=self.City.data,
            Rating=self.Rating.data,
			Year=self.Year.data,
			CreatedOn=self.CreatedOn.data,
            product_idIdFk=self.Product.data
        )
