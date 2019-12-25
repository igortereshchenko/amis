from flask_wtf import Form
from wtforms import SelectField, SubmitField, DateField, HiddenField, IntegerField
from datetime import date
from wtforms import validators
from wtforms.validators import NumberRange
from source.dao.db import PostgresDb
import source.dao.orm.entities as entities


class RecordBook(Form):
    discipline_id = HiddenField()

    professor_id = HiddenField()

    professor_chose = SelectField("Professor:", coerce=int)

    discipline_chose = SelectField("Discipline:", coerce=int)

    semester_mark = IntegerField("semester point: ", [
        validators.DataRequired("Please enter semester point"), NumberRange(min=0, max=60, message='number range '
                                                                                                   'between 0 and 60')],
                                 default=0)

    final_mark = IntegerField("final point: ", [NumberRange(min=0, max=100, message='number range between 0 and 100')],
                              default=0)

    exam_passed = DateField("passed date: ", [
        validators.DataRequired("Please enter passed date")], format='%d-%b-%y', default=date.today())

    submit = SubmitField("Save")

    def __init__(self, uni, faculty, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

        db = PostgresDb()
        professors = db.sqlalchemy_session.query(entities.Professor). \
            filter(entities.Professor.professor_date_expelled == None,
                   entities.Professor.professor_university == uni).all()
        disciplines = db.sqlalchemy_session.query(entities.Discipline).filter(
            entities.Discipline.discipline_university == uni, entities.Discipline.discipline_faculty == faculty).all()

        self.professor_chose.choices = [(professor.professor_id,
                                         "name: '{}'; surname: '{}'; "
                                         "department: '{}'".format(professor.name,
                                                                   professor.surname,
                                                                   professor.professor_department))
                                        for professor in professors]

        self.discipline_chose.choices = [(discipline.discipline_id,
                                          "name: '{}'; exam: '{}'".format(discipline.discipline_name,
                                                                          discipline.discipline_exam))
                                         for discipline in disciplines]
