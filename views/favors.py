from wtforms import DateTimeField, SubmitField, validators, SelectField
from flask_wtf import FlaskForm
from domain import models


class FavorsViewModel(FlaskForm):
    Clothe = SelectField("clothe", validators=[validators.DataRequired()])
    Vendor = SelectField("vendor", validators=[validators.DataRequired()])
    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Favors(
            vendor_idIdFk=self.Vendor.data,
            clothe_idIdFk=self.Clothe.data,
            CreatedOn=self.CreatedOn.data
        )