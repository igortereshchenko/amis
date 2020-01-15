from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms import validators

from dao.db import PostgresDB
from dao.orm.model import ormTest, ormQuestion

db = PostgresDB()


def test_choices():
    return db.sqlalchemy_session.query(ormTest).all()


def test_question_choices():
    return db.sqlalchemy_session.query(ormQuestion).all()


class TestForm(FlaskForm):
    test_name = StringField("Name: ", [validators.DataRequired(), validators.Length(max=63)])
    test_variant = IntegerField('Variant: ')
    submit = SubmitField("Save")


class QuestionForm(FlaskForm):
    question_text = StringField("Name: ", [validators.DataRequired(), validators.Length(max=63)])
    test_id = IntegerField()
    submit = SubmitField("Save")


class QuestionVariantForm(FlaskForm):
    answer_variant_text = StringField("Name: ", [validators.DataRequired(), validators.Length(max=511)])
    question_id = IntegerField()


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email', validators=[validators.DataRequired('Please enter a valid email address.'),
                                             validators.Email('Please enter a valid email address.')])
    password = PasswordField('Password', validators=[validators.DataRequired('Uhh, your password tho?')])
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    """User Signup Form."""
    first_name = StringField('First name', validators=[validators.DataRequired(message=('First name must be not empty'))])
    last_name = StringField('Last name', validators=[validators.DataRequired(message=('Last name must be not empty.'))])

    email = StringField('Email',
                        validators=[validators.Length(min=6, message=('Email length must be > 6.')),
                                    validators.Email(message=('Please enter a valid email address.')),
                                    validators.DataRequired(message=('Email is required field.'))])
    password = PasswordField('Password',
                             validators=[validators.DataRequired(message='Please enter a password.'),
                                         validators.Length(min=6, message=('Please select a stronger password.')),
                                         validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Your Password',)

    submit = SubmitField('Register')


class UserUpdateForm(FlaskForm):
    first_name = StringField('First name', validators=[validators.DataRequired(message=('First name must be not empty'))])
    last_name = StringField('Last name', validators=[validators.DataRequired(message=('Last name must be not empty.'))])

    role = StringField('Role', validators=[validators.DataRequired(message=('Role must be not empty'))])

    submit = SubmitField('Register')