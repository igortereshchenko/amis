from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, DateField, IntegerField, DateTimeField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Regexp, EqualTo
from datetime import date, datetime

class LoginForm(FlaskForm):
    """Login form"""
    name = StringField('Name',[
        DataRequired('Enter name'), Length(2,20,"Name should be from 2 to 20 chars")])
    password = PasswordField('Password', [
        DataRequired('Enter password')])

    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    """Registration"""
    name = StringField('Name', [
        DataRequired('Enter name'), Length(2, 20, "Name should be from 2 to 20 chars")])
    age = DateField('Birthday', default=date.today())
    weight = IntegerField('Weight', [
        DataRequired('Enter weight - should be from 10 to 900'), NumberRange(min=10, max=900)])
    hight = IntegerField('Height', [
        DataRequired('Enter height - should be from 30 to 400'), NumberRange(min=30, max=400)])
    password = PasswordField('Password', [
        DataRequired('Enter password')])
    confirm = PasswordField('Confirm password', [
        DataRequired('Reenter correct password'), EqualTo('password')])

    submit = SubmitField('Submit')

class ComplexForm(FlaskForm):
    """Complex CRUD"""
    name = StringField('Complex name', [
        DataRequired("Enter name complex"), Length(2, 20, "Name should be from 2 to 20 chars")])
    level = SelectField('Complex level', choices=[('light','light'), ('middle','middle'), ('hard', 'hard')])
    submit = SubmitField('Submit')
# ,  Regexp('^(done|rejected|awaiting)$', message='Enter done or rejected or awaiting')

class ExerciseForm(FlaskForm):
    """Exercise CRUD"""
    name = StringField('Exercise name', [
        DataRequired("Enter exercise"), Length(2, 20, "should be from 2 to 20 chars")])
    info = StringField('Image Url', [
        DataRequired('insert url')])

    submit = SubmitField('Submit')


class CheForm(FlaskForm):
    "CHE CRUD"
    complex_name = StringField('Complex name', [
        DataRequired("Enter name complex"), Length(2, 20, "Name should be from 2 to 20 chars")])
    exercise_name = StringField('Exercise name', [
        DataRequired("Enter exercise"), Length(2, 20, "should be from 2 to 20 chars")])
    repeater = IntegerField('Repeat times', [
        DataRequired("How many times to repeat?"), NumberRange(min=1, max=500)])

    submit = SubmitField('Submit')

class Update(FlaskForm):
    "UPD form"

    weight = IntegerField('Weight', [
        DataRequired('Enter weight - should be from 10 to 900'), NumberRange(min=10, max=900)])
    hight = IntegerField('Height', [
        DataRequired('Enter height - should be from 30 to 400'), NumberRange(min=30, max=400)])
    submit = SubmitField('Submit')