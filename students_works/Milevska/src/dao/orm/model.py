from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from dao.db import PostgresDB
from flask_login import UserMixin, current_user

db = PostgresDB()

Base = declarative_base()


class ormDiscipline(Base):
    __tablename__ = 'orm_discipline'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    questions = relationship('ormQuestion', cascade="all,delete")


class ormTest(Base):
    __tablename__ = 'orm_test'

    test_id = Column(Integer, primary_key=True, autoincrement=True)
    test_name = Column(String(63), nullable=False)

    orm_questions = relationship('ormQuestion', cascade="all,delete")

    def __init__(self, test_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_name = test_name


class ormQuestion(Base):
    __tablename__ = 'orm_question'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(String(511), nullable=False)
    test_id = Column(Integer, ForeignKey('orm_test.test_id'))
    discipline_id = Column(Integer, ForeignKey('orm_discipline.id'), nullable=True)

    answer_variants = relationship('ormAnswerVariant', cascade="all,delete")


class ormAnswerVariant(Base):
    __tablename__ = 'orm_answer_variant'

    answer_variant_id = Column(Integer, primary_key=True, autoincrement=True)
    answer_variant_text = Column(String(511), nullable=False)
    answer_check = Column(Boolean, default=False, nullable=False)
    question_id = Column(Integer, ForeignKey('orm_question.question_id', ondelete='CASCADE'))


class ormUser(UserMixin, Base):
    __tablename__ = 'orm_user'

    USER_ROLES = ['ADMIN', 'STANDARD']

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(80), unique=True)
    password = Column(String(80))
    role = Column(String(10), server_default='STANDARD', default='STANDARD')
    first_name = Column(String(80))
    last_name = Column(String(80))

    def __init__(self, email, password, role, first_name, last_name):
        self.email = email
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)

    def set_password(self, password):
        return generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

