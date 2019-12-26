from sqlalchemy import Column, String, Integer, Date, ForeignKey

from LecturebotDAL.dbcontext import ModelBase

class Student(ModelBase):

    __tablename__ = 'student'
    gradebook_number = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    stgroup = Column(String)
    year_of_receipt = Column(Date)
    def __init__(self, gradebook_number,full_name,stgroup,year_of_receipt):
        self.gradebook_number = gradebook_number
        self.full_name = full_name
        self.stgroup = stgroup
        self.year_of_receipt = year_of_receipt

    def to_string(self):
        return "Name: " + self.full_name + " " ", Group: " + self.stgroup


class Teacher(ModelBase):
    __tablename__ = 'teacher'

    pass_number = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    department = Column(String)

    def __init__(self, pass_number, full_name, department):
        self.pass_number = pass_number
        self.full_name = full_name
        self.department = department


class CourseWork(ModelBase):

    __tablename__ = 'course_work'

    initalization_num = Column(Integer, primary_key=True)
    gradebook_number = Column(Integer, ForeignKey('student.gradebook_number'))
    cwname = Column(String, nullable=False)
    research_direction = Column(String)
    mark = Column(Integer)


    def __init__(self, initalization_num,gradebook_number,cwname,research_direction,mark):
        self.initalization_num = initalization_num
        self.gradebook_number = gradebook_number
        self.cwname = cwname
        self.research_direction = research_direction
        self.mark = mark


    def to_string(self):
        return "Research direction: " + self.research_direction + " (" + self.cwname + "), gradebook number: " + self.gradebook_number

class Subject(ModelBase):

    __tablename__ = 'subject'

    pass_num = Column(Integer, primary_key=True)
    sbname = Column(String, nullable=False)
    student_rating = Column(Integer)
    gradebook_number = Column(Integer, ForeignKey('student.gradebook_number'))
    pass_number = Column(Integer, ForeignKey('teacher.pass_number'))


    def __init__(self,pass_num ,sbname ,student_rating ,gradebook_number,pass_number ):
        self.pass_num = pass_num
        self.sbname = sbname
        self.student_rating = student_rating
        self.gradebook_number = gradebook_number
        self.pass_number = pass_number
    def to_string(self):
        return "Subject: " + self.sbname + " Teacher:(" + self.pass_numbe + ")"
		


class House(ModelBase):

    __tablename__ = 'house'

    build_num = Column(Integer, primary_key=True)
    adress = Column(String)
    floors = Column(Integer, nullable=False)
    years = Column(Integer)
    #pass_number = Column(Integer, ForeignKey('teacher.pass_number'))

    def __init__(self, build_num, adress,floors,years):
        self.build_num = build_num
        self.adress =  adress
        self.floors = floors
        self.years = years
        #self.pass_number = pass_number
		
		

