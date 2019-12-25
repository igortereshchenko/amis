from flask_wtf import Form
from wtforms import SelectField, SubmitField, BooleanField
from sqlalchemy import func
from datetime import date
from source.dao.db import PostgresDb
from source.dao.orm.entities import StudentRecordBook


class RecordSearchForm(Form):
    year = SelectField("year:", coerce=int)
    semester = SelectField("semester:", coerce=int)
    submit = SubmitField("Search")

    def __init__(self, dates, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

        self.year.choices = [(year, "{}-{}".format(year, year + 1)) for year in dates]

        self.semester.choices = [(1, "first semester"), (2, "second semester")]

    def search(self, student_id):
        db = PostgresDb()

        if int(self.semester.data) == 1:
            records = db.sqlalchemy_session.query(StudentRecordBook).filter(
                StudentRecordBook.exam_passed.between(date(int(self.year.data), 9, 1),
                                                      date(int(self.year.data) + 1, 1, 31)),
                StudentRecordBook.student_id_fk == student_id).all()
        else:
            records = db.sqlalchemy_session.query(StudentRecordBook).filter(
                StudentRecordBook.exam_passed.between(date(int(self.year.data) + 1, 1, 1),
                                                      date(int(self.year.data) + 1, 8, 31)),
                StudentRecordBook.student_id_fk == student_id).all()

        return records
