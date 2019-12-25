from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, SelectField, StringField, PasswordField

from model import model
from model.university_faculties import university_faculties


class UniversityUserForm(FlaskForm):
    UserFullName = StringField("user_fullname", [validators.DataRequired("Enter user's fullname")])
    User_email = StringField("user_email", [validators.DataRequired("Enter user's email")])
    User_password = PasswordField("user_password", validators=[validators.DataRequired("Enter user's password")])
    User_faculty = SelectField("user_faculty", validators=[validators.DataRequired()], choices=university_faculties)

    Submit = SubmitField("Save")

    def model(self):
        return model.UniversityUsersTable(
            UserFullName=self.UserFullName.data,
            User_email=self.User_email.data,
            User_password=self.User_password.data,
            User_faculty=self.User_faculty.data
        )
