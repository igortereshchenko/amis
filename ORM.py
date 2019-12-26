from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jvehmagztyojdu:50a71e72bae8b4452ef0fc0f4b527617df7f199870aa772fdfb91f743cfdd0a2@ec2-54-228-207-163.eu-west-1.compute.amazonaws.com:5432/d2fqinb643acpv'

db = SQLAlchemy(app)


class Groups(db.Model):

    __tablename__ = 'groups'
    code = db.Column('code', db.String(64), primary_key=True)
    students = db.relationship('Students', backref='groups', lazy='dynamic')
    group_subject = db.relationship('GroupSubject', backref='groups', lazy='dynamic')

    def __init__(self, code):

        self.code = code

    def __repr__(self):

        return '<Group: code=%r>' % self.code


class Subjects(db.Model):

    __tablename__ = 'subjects'
    name = db.Column('name', db.String(64), primary_key=True)
    group_subject = db.relationship('GroupSubject', backref='subjects', lazy='dynamic')
    subjects_marks = db.relationship('SubjectsMarks', backref='subjects', lazy='dynamic')
    subjectsheet = db.relationship('SubjectSheet', backref='subjects', lazy='dynamic')

    def __init__(self, name):

        self.name = name

    def __repr__(self):

        return 'Subject: name=%r' % self.name


class StudentStatus(db.Model):

    __tablename__ = 'studentstatus'
    group_code = db.Column('group_code', db.String(64), db.ForeignKey('students.group_code'), primary_key=True)
    study_book = db.Column('study_book', db.String(64), db.ForeignKey('students.study_book'), primary_key=True)
    actual_date = db.Column('actual_date', db.String(64), primary_key=True)
    status = db.Column('status', db.String(64))
    destiny = db.Column('destiny', db.String(64))
    student_group = db.relationship('Students', backref='status_group', lazy=True,
                              foreign_keys=[group_code])
    student_spook = db.relationship('Students', backref='status_spook', lazy=True,
                              foreign_keys=[study_book])

    def __init__(self, study_book, group_code, actual_date, status, destiny):

        self.study_book = study_book
        self.group_code = group_code
        self.actual_date = actual_date
        self.status = status
        self.destiny = destiny

    def __repr__(self):

        return '<StudentStatus: study_book=%r; group_code=%r; actual_date=%r; status=%r; destiny=%r>' %\
               self.study_book, self.group_code, self.actual_date, self.status, self.destiny


class SubjectSheet(db.Model):

    __tablename__ = 'subjectsheet'
    subj_name = db.Column('subj_name', db.String(64), db.ForeignKey('subjects.name'), primary_key=True)
    group_code = db.Column('group_code', db.String(64), db.ForeignKey('students.group_code'), primary_key=True)
    study_book = db.Column('study_book', db.String(64), db.ForeignKey('students.study_book'), primary_key=True)
    date_of_mark = db.Column('date_of_mark', db.Date, primary_key=True)
    mark = db.Column('mark', db.Float, nullable=False)
    student_group = db.relationship('Students', backref='sheet_group', lazy=True,
                              foreign_keys=[group_code])
    student_spook = db.relationship('Students', backref='sheet_spook', lazy=True,
                              foreign_keys=[study_book])

    def __init__(self, subj_name, group_code, study_book, date_of_mark, mark):

        self.subj_name = subj_name
        self.group_code = group_code
        self.study_book = study_book
        self.date_of_mark = date_of_mark
        self.mark = mark

    def __repr__(self):

        return '<SubjectSheet: subj_name=%r; group_code=%r; study_book=%r; date_of_mark=%r; mark=%r>' %\
               self.subj_name, self.group_code, self.study_book, self.date_of_mark, self.mark


class GroupSubject(db.Model):

    __tablename__ = 'group_subject'
    group_code = db.Column('group_code', db.String(64), db.ForeignKey('groups.code'), primary_key=True)
    subj_name = db.Column('subj_name', db.String(64), db.ForeignKey('subjects.name'), primary_key=True)
    year = db.Column('year', db.Integer, primary_key=True)
    semester = db.Column('semester', db.Integer, primary_key=True)

    def __init__(self, group_code, subj_name, year, semester):

        self.group_code = group_code
        self.subj_name = subj_name
        self.year = year
        self.semester = semester

    def __repr__(self):

        return '<GroupSubject: group_code=%r; subj_name=%r; year=%r; semester=%r>' %\
               self.group_code, self.subj_name, self.year, self.semester


class SubjectsMarks(db.Model):

    __tablename__ = 'subjects_marks'

    subj_name = db.Column('subj_name', db.String(64), db.ForeignKey('subjects.name'), primary_key=True)
    curr_max_mark = db.Column('curr_max_mark', db.String(64))
    actual_date = db.Column('actual_date', db.Date, primary_key=True)

    def __init__(self, subj_name, curr_max_mark, actual_date):

        self.subj_name = subj_name
        self.curr_max_mark = curr_max_mark
        self.actual_date = actual_date

    def __repr__(self):

        return '<SubjectsMarks: subj_name=%r; curr_max_mark=%r; actual_date=%r>' %\
               self.subj_name, self.curr_max_mark, self.actual_date


class Students(db.Model):

    __tablename__ = 'students'
    first_name = db.Column('first_name', db.String(64), nullable=False)
    last_name = db.Column('last_name', db.String(64), nullable=False)
    study_book = db.Column('study_book', db.String(64), primary_key=True)
    group_code = db.Column('group_code', db.String(64), db.ForeignKey('groups.code'), primary_key=True)

    def __init__(self, first_name, last_name, study_book, group_code):

        self.first_name = first_name
        self.last_name = last_name
        self.study_book = study_book
        self.group_code = group_code

    def __repr__(self):

        return '<Student: first_name=%r; last_name=%r; study_book=%r; group_code=%r>' % \
               self.first_name, self.last_name, self.study_book, self.group_code
