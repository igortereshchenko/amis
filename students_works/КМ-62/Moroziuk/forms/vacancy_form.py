from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, validators, SubmitField, IntegerField, SelectField
from wtforms.widgets import html5


class VacancyForm(FlaskForm):
    id = HiddenField("Id")

    name = StringField("Vacancy name: ",[
        validators.DataRequired("Please enter name."),
    ])

    duties = StringField("Duties: ",[
        validators.DataRequired("Please enter duties."),
    ])

    salary = IntegerField("Salary: ", widget=html5.NumberInput()
    )

    description = StringField("Description: ", [
        validators.DataRequired("Please enter description."),
    ])

    profession_id = SelectField("profession: ", choices=[], coerce=int)  # ,[validators.DataRequired(),])

submit = SubmitField("Save")