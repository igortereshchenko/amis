from wtforms import StringField, DateTimeField, SubmitField, validators
from flask_wtf import FlaskForm
from domain import models


class SchemaForm(FlaskForm):
    Id = StringField("Id")
    Name = StringField("Name", [validators.DataRequired("Schema name is required")])
    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Schemas(
            Name=self.Name.data,
            CreatedOn=self.CreatedOn.data
        )
