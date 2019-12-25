from flask_wtf import Form
from wtforms import SelectField, SubmitField
from sqlalchemy import func
from source.dao.db import PostgresDb
from source.dao.orm.entities import Student, Professor, StudentRecordBook, Discipline


class StudentSearchRecordForm(Form):
    student_name = SelectField("student name:", choices=[("", "---")])
    student_surname = SelectField("student surname:", choices=[("", "---")])
    student_group = SelectField("student group:", choices=[("", "---")])
    discipline_university = SelectField("discipline university:", choices=[("", "---")])
    discipline_faculty = SelectField("discipline faculty:", choices=[("", "---")])
    discipline_name = SelectField("discipline name:", choices=[("", "---")])
    discipline_hours_for_semester = SelectField("discipline hours for semester:", choices=[("", "---")])
    discipline_exam = SelectField("discipline exam:", choices=[("", "---")])
    professor_name = SelectField("professor name:", choices=[("", "---")])
    professor_surname = SelectField("professor surname:", choices=[("", "---")])
    professor_degree = SelectField("professor degree:", choices=[("", "---")])
    submit = SubmitField("Search")

    def init(self):
        db = PostgresDb()

        self.student_name.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.name).distinct(Student.name).all())]

        self.student_surname.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.surname).distinct(Student.surname).all())]

        self.student_group.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_group).distinct(Student.student_group).all())]

        self.discipline_university.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Discipline.discipline_university).distinct(
                Discipline.discipline_university).all())]

        self.discipline_faculty.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Discipline.discipline_faculty).distinct(Discipline.discipline_faculty).all())]

        self.discipline_name.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Discipline.discipline_name).distinct(Discipline.discipline_name).all())]

        self.professor_name.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Professor.name).distinct(Professor.name).all())]

        self.professor_surname.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Professor.surname).distinct(Professor.surname).all())]

        self.professor_degree.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Professor.professor_degree).distinct(Professor.professor_degree).all())]

        self.discipline_hours_for_semester.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Discipline.discipline_hours_for_semester).distinct(
                Discipline.discipline_hours_for_semester).all())]

        self.discipline_exam.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Discipline.discipline_exam).distinct(Discipline.discipline_exam).all())]

    def search(self, method):
        db = PostgresDb()

        query = db.sqlalchemy_session.query(StudentRecordBook.semester_mark,
                                            StudentRecordBook.final_mark).distinct(
            StudentRecordBook.semester_mark,
            StudentRecordBook.final_mark).filter(StudentRecordBook.final_mark != 0)

        if method == 'POST':
            if self.student_name.data and self.student_name.data != "None":
                student_id = [i[0] for i in db.sqlalchemy_session.query(Student.student_id).filter(
                    Student.name == self.student_name.data).all()]
                query = query.filter(StudentRecordBook.student_id_fk.in_(student_id))
            if self.student_surname.data and self.student_surname.data != "None":
                student_id = [i[0] for i in db.sqlalchemy_session.query(Student.student_id).filter(
                    Student.surname == self.student_surname.data).all()]
                query = query.filter(StudentRecordBook.student_id_fk.in_(student_id))
            if self.student_group.data and self.student_group.data != "None":
                student_id = [i[0] for i in db.sqlalchemy_session.query(Student.student_id).filter(
                    Student.student_group == self.student_group.data).all()]
                query = query.filter(StudentRecordBook.student_id_fk.in_(student_id))

            if self.discipline_university.data and self.discipline_university.data != "None":
                discipline_id = [i[0] for i in db.sqlalchemy_session.query(Discipline.discipline_id).filter(
                    Discipline.discipline_university == self.discipline_university.data).all()]
                query = query.filter(StudentRecordBook.discipline_id_fk.in_(discipline_id))
            if self.discipline_faculty.data and self.discipline_faculty.data != "None":
                discipline_id = [i[0] for i in db.sqlalchemy_session.query(Discipline.discipline_id).filter(
                    Discipline.discipline_faculty == self.discipline_faculty.data).all()]
                query = query.filter(StudentRecordBook.discipline_id_fk.in_(discipline_id))
            if self.discipline_name.data and self.discipline_name.data != "None":
                discipline_id = [i[0] for i in db.sqlalchemy_session.query(Discipline.discipline_id).filter(
                    Discipline.discipline_name == self.discipline_name.data).all()]
                query = query.filter(StudentRecordBook.discipline_id_fk.in_(discipline_id))
            if self.discipline_hours_for_semester.data and self.discipline_hours_for_semester.data != "None":
                discipline_id = [i[0] for i in db.sqlalchemy_session.query(Discipline.discipline_id).filter(
                    Discipline.discipline_hours_for_semester == self.discipline_hours_for_semester.data).all()]
                query = query.filter(StudentRecordBook.discipline_id_fk.in_(discipline_id))
            if self.discipline_exam.data and self.discipline_exam.data != "None":
                discipline_id = [i[0] for i in db.sqlalchemy_session.query(Discipline.discipline_id).filter(
                    Discipline.discipline_exam == self.discipline_exam.data).all()]
                query = query.filter(StudentRecordBook.discipline_id_fk.in_(discipline_id))

            if self.professor_name.data and self.professor_name.data != "None":
                professor_id = [i[0] for i in db.sqlalchemy_session.query(Professor.professor_id).filter(
                    Professor.name == self.professor_name.data).all()]
                query = query.filter(StudentRecordBook.professor_id_fk.in_(professor_id))
            if self.professor_surname.data and self.professor_surname.data != "None":
                professor_id = [i[0] for i in db.sqlalchemy_session.query(Professor.professor_id).filter(
                    Professor.surname == self.professor_surname.data).all()]
                query = query.filter(StudentRecordBook.professor_id_fk.in_(professor_id))
            if self.professor_degree.data and self.professor_degree.data != "None":
                professor_id = [i[0] for i in db.sqlalchemy_session.query(Professor.professor_id).filter(
                    Professor.professor_degree == self.professor_degree.data).all()]
                query = query.filter(StudentRecordBook.professor_id_fk.in_(professor_id))

        return query.all()
