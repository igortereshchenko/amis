from sqlalchemy import Column, Integer, String, Date, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = 'Student'

    name = Column(String, primary_key=True)
    sgroup = Column(Integer, primary_key=True)


class Teacher(Base):
    __tablename__ = 'Teacher'

    name = Column(String, primary_key=True)
    degree = Column(String(255), nullable=False)


class Discipline(Base):
    __tablename__ = 'Discipline'

    name = Column(String(255), primary_key=True)
    teacher_name = Column(String(255), ForeignKey('Teacher.name'))

    teacher_entity = relationship("Teacher")


class Task(Base):
    __tablename__ = 'Task'

    id = Column(Integer)
    name = Column(String(255), nullable=False , primary_key=True)
    discipline_name = Column(String(255), ForeignKey('Discipline.name'))
    value = Column(Integer, nullable=False)
    deadline = Column(Date, nullable=False)

    discipline_entity = relationship("Discipline")


class Student_Discipline(Base):
    __tablename__ = 'Student_Discipline'
    discipline_name = Column(String(255), ForeignKey('Discipline.name'), primary_key=True)
    student_name = Column(String(255), primary_key=True)
    student_group = Column(Integer, primary_key=True)
    points = Column(Integer, nullable=False)

    discipline_entity = relationship("Discipline")
    student_entity = relationship("Student")
    __table_args__ = (ForeignKeyConstraint([student_name, student_group],
                                           [Student.name,
                                            Student.sgroup]), {})


class Student_Task(Base):
    __tablename__ = 'Student_Task'
    task_id = Column(Integer, ForeignKey('Task.id'), primary_key=True)
    student_name = Column(String(255), primary_key=True)
    student_group = Column(Integer, primary_key=True)

    student_entity = relationship("Student")
    task_entity = relationship("Task")
    __table_args__ = (ForeignKeyConstraint([student_name, student_group],
                                           [Student.name,
                                            Student.sgroup]),
                      {})

class Users(Base):
    __tablename__= 'Users'
    name = Column(String(255),primary_key=True)
    password = Column(String(255),primary_key=True)
    sgroup = Column(Integer)

    student_entity = relationship("Student")
    __table_args__ = (ForeignKeyConstraint([name, password],
                                           [Student.name,
                                            Student.sgroup]),
                      {})

if __name__ == '__main__':
    from dao.db import PostgresDb

    db = PostgresDb()
    # simple query test
    q1 = db.sqlalchemy_session.query(Discipline).all()
    for q in q1:
        print(q)
    q2 = db.sqlalchemy_session.query(Student).all()
    q3 = db.sqlalchemy_session.query(Task).all()
    q4 = db.sqlalchemy_session.query(Student_Task).join(Student).join(Task).all()
    q5 = db.sqlalchemy_session.query(Student_Discipline).join(Student).join(Discipline).all()
    q5 = db.sqlalchemy_session.query(Users).all()
    print()
