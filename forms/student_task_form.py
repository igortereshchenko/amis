from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, HiddenField, TimeField
from wtforms import validators


class Student_TaskForm(Form):

    task_id = IntegerField("Task id: ", [
        validators.DataRequired("Please enter task id.")])

    student_name = StringField("Student Name: ", [
        validators.DataRequired("Please enter student name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])
    student_group = IntegerField("Group: ", [
        validators.DataRequired("Please enter student Group.")])

    old_id = HiddenField()
    old_name = HiddenField()
    old_group = HiddenField()


    submit = SubmitField("Save")
