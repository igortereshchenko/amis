from wtforms import StringField, DateTimeField, SubmitField, BooleanField, SelectField, validators
from flask_wtf import FlaskForm
from domain import models


class EntityForm(FlaskForm):
    Id = StringField("Id")
    Name = StringField("Name", [validators.DataRequired("Entity name is required")])
    IsOverrideExisted = BooleanField("Override Existed?", default=False)
    CreatedOn = DateTimeField("Created On")
    Schema = StringField("Schema")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Entities(
            Name=self.Name.data,
            IsOverrideExisted=self.IsOverrideExisted.data,
            CreatedOn=self.CreatedOn.data
        )
