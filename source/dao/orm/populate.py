from source.dao.orm.entities import *
from source.dao.db import PostgresDb
import numpy as np
import pandas as pd
import datetime


def populate(path=''):
    semester_min = 10
    exam_min = 23

    db = PostgresDb()

    session = db.sqlalchemy_session

    df = pd.read_csv(path + "exams_list.csv", sep=',')

    df = df[df["Exam points"] > exam_min]
    df["Semester points"] = df["Exam points"] - np.random.randint(0, 40, size=(df.shape[0]))

    df["Semester points"] = np.where(df["Semester points"] < 0, 0, df["Semester points"])
    df["Semester points"] = np.where(df["Semester points"] > 60, 60, df["Semester points"])

    best_val = df["Semester points"] == 60

    df1, df2 = df[~best_val], df[best_val]
    # part_1, part_2 = np.array_split(df2, 2)
    # df = pd.concat([df1, part_1])
    df_best = df2.sample(frac=0.4)
    df = pd.concat([df1, df_best])

    df = df[df["Semester points"] > semester_min]

    students, names = [], set()
    records = []

    uni = [str(u[0]) for u in
           db.sqlalchemy_session.query(Student.student_university).distinct(Student.student_university).all()]

    id = max([int(i[0]) for i in db.sqlalchemy_session.query(Student.student_id).all()])

    for index, row in df.iterrows():
        name = row["Student name"].split(' ')

        if name[0] not in names:
            id += 1
            names.add(name[0])
            uni_ch = np.random.choice(uni, 1)[0]
            faculty = [str(f[0]) for f in
                       db.sqlalchemy_session.query(Student.student_faculty).distinct(Student.student_faculty).filter(
                           Student.student_university == uni_ch).all()]
            faculty_ch = np.random.choice(faculty, 1)[0]
            group = [str(g[0]) for g in
                     db.sqlalchemy_session.query(Student.student_group).distinct(Student.student_group).filter(
                         Student.student_university == uni_ch,
                         Student.student_faculty == faculty_ch).all()]

            professors = [int(p[0]) for p in
                db.sqlalchemy_session.query(Professor.professor_id).filter(Professor.professor_university
                                                                       == uni_ch).all()]
            disciplines = [int(d[0]) for d in
            db.sqlalchemy_session.query(Discipline.discipline_id).filter(
                Discipline.discipline_university == uni_ch,
                Discipline.discipline_faculty == faculty_ch).all()]

            students.append(Student(
                student_university=uni_ch,
                student_faculty=faculty_ch,
                student_group=np.random.choice(group, 1)[0],
                name=name[0],
                surname=name[1],
                login=name[0],
                password=name[0],
                student_date_expelled=datetime.date.today(),
            ))

            records.append(StudentRecordBook(
                student_id_fk=id,
                discipline_id_fk=np.random.choice(disciplines, 1)[0],
                professor_id_fk=np.random.choice(professors, 1)[0],
                semester_mark=row["Semester points"],
                final_mark=row["Exam points"],
                exam_passed=datetime.date.today(),
            ))

    # insert into database
    session.add_all(students)
    # session.commit()
    session.add_all(records)
    session.commit()


if __name__ == '__main__':
    populate()
