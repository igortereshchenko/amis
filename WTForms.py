from flask_wtf import Form
from wtforms import StringField, FloatField, SubmitField, DateField, Label
from wtforms import validators


class GroupsForm(Form):

    code = StringField("Code: ", [validators.data_required("Please, enter a code of the group.")])

    submit = SubmitField("Enter")


class SubjectsForm(Form):

    name = StringField("Name: ", [validators.data_required("Please, enter a name of the subject.")])

    submit = SubmitField("Enter")


class StudentsForm(Form):

    first_name = StringField("First name: ", [validators.data_required("Please, enter a first name of the student.")])
    last_name = StringField("Last name: ", [validators.data_required("Please, enter a last name of the student.")])
    study_book = StringField("Study book: ", [validators.data_required("Please, enter a study book of the student.")])
    group_code = StringField("Group code: ", [validators.data_required("Please, enter a group code of the student.")])

    submit = SubmitField("Enter")


class SubjectSheetForm(Form):

    subj_name = StringField("Subject Name: ", [validators.data_required("Please, enter a name of the subject.")])
    group_code = StringField("Group code: ", [validators.data_required("Please, enter a group code of the student.")])
    study_book = StringField("Study book: ", [validators.data_required("Please, enter a study book of the student.")])
    date_of_mark = DateField("Date of Mark: ", [validators.data_required("Please, enter a date of the mark.")])
    mark = FloatField("Mark: ", [validators.data_required("Please, enter the mark.")])

    submit = SubmitField("Enter")