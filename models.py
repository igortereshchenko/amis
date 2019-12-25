from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    user_name = Column(String(20), primary_key=True)
    age = Column(Date, nullable=False)
    pasword = Column(String(20), nullable=False)

class Complex(Base):
    __tablename__ = 'complex'

    complex_name = Column(String(20), primary_key=True)
    complex_level = Column(String(20), nullable=False)

class Exercise(Base):
    __tablename__ = 'exercise'

    exercise_name = Column(String(20), primary_key=True)
    information = Column(String(500), nullable=False)

class Complex_has_exercise(Base):
    __tablename__ = 'complex_has_exercise'

    complex_name = Column(String(20), ForeignKey('complex.complex_name'), primary_key=True)
    exercise_name = Column(String(20), ForeignKey('exercise.exercise_name'), primary_key=True)
    repeater = Column(Integer, nullable=False)

class Activate(Base):
    __tablename__ = 'activate'

    user_name = Column(String(20), ForeignKey('users.user_name'), primary_key=True)
    complex_name = Column(String(20), ForeignKey('complex.complex_name'), primary_key=True)
    time_start = Column(DateTime, primary_key=True)
    status = Column(String(10), nullable=False)
    weight = Column(Integer, nullable=False)
    hight = Column(Integer, nullable=False)