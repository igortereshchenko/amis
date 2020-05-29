from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
import datetime
import math

Base = declarative_base()


class Group(Base):
    __tablename__ = 'Groups1'

    group_id = Column(Integer, primary_key=True)
    group_faculty = Column(String(255), nullable=False)
    group_name = Column(String(255), nullable=False)

    scedule_entity = relationship("Scedule", cascade = "delete")



class Apply(Base):
    __tablename__ = 'Apply'

    user_id = Column(Integer, primary_key=True)
    user_email = Column(String(255), nullable=False, unique=True)
    user_pass = Column(String(255), nullable=False)


class Teacher(Base):
    __tablename__ = 'Teachers1'

    teacher_id = Column(Integer, primary_key=True)
    teach_name = Column(String(255), nullable=False)
    teach_faculty = Column(String(255), nullable=False)

    scedule_entity = relationship("Scedule", cascade = "delete")



class Subject(Base):
    __tablename__ = 'Subjects1'

    subj_name = Column(String(255), primary_key=True)
    subj_hours = Column(Integer, nullable=True)

    scedule_entity = relationship("Scedule", cascade = "delete")



class Scedule(Base):
    __tablename__ = 'Schedule1'

    group_id_fk = Column(Integer, primary_key=True)
    subj_name_fk = Column(String(255), nullable=True)
    teach_id_fk = Column(Integer, nullable=True)
    times = Column(Date, primary_key=True)
    days = Column(String, primary_key = True)
    auditorium = Column(String(255), nullable=True)

    __table_args__ = (ForeignKeyConstraint([group_id_fk], [Group.group_id]), ForeignKeyConstraint([subj_name_fk], [Subject.subj_name]), ForeignKeyConstraint([teach_id_fk], [Teacher.teacher_id]), {})






if __name__ == '__main__':
    from dao.db import PostgresDb

    db = PostgresDb()
    # simple query test
    # q1 = db.sqlalchemy_session.query(Subject).all()
    # q2 = db.sqlalchemy_session.query(Scedule).all()



    for key in table:
        print(str(key) + " is class " + table[key])


