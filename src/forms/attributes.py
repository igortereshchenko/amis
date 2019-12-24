from wtforms import StringField, DateTimeField, SubmitField, BooleanField, SelectField, validators
from flask_wtf import FlaskForm
from domain import models
from domain.layout import data_types


class AttributeViewModel(FlaskForm):
    Name = StringField("Name", [validators.DataRequired("Attribute name is required")])
    Type = SelectField("Type", [validators.DataRequired("Attribute type is required")],
                       choices=data_types)
    IsNull = BooleanField("Nullable?", default=True)
    IsPrimaryKey = BooleanField("Is a primary key part?", default=False)
    CreatedOn = DateTimeField("Created On")
    Entity = StringField("Entity")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Attributes(
            self.Name.data,
            self.Type.data,
            self.IsNull.data,
            self.IsPrimaryKey.data
        )
