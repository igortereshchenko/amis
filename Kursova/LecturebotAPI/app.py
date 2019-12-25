import os
import math

from flask import Flask, render_template, request, redirect

from LecturebotDAL.repository.dataservice import get_data, update_data_t, get_data_by, update_data_s,update_data_cw, get_data_class, delete_data_passn, get_data_by_passn, delete_data_build_num, update_data_b, insert_data,get_data_by_build_num, get_data_by_id, delete_data, save, update_data, req1, req2, req3,get_data_by_init, get_data_by_pass, delete_data_init, delete_data_pass
from LecturebotDAL.models.model import Student, CourseWork, Subject,  Teacher, House
from LecturebotAPI.forms.Student_form import Studform
from LecturebotAPI.forms.Student_coursework_form import CourseworkForm
from LecturebotAPI.forms.Teacher_form import TeacherForm
from LecturebotAPI.forms.Subject_form import Subj_form
from LecturebotAPI.forms.House_form import HouseForm
from LecturebotAPI.forms.Class import Classform
from wtforms.fields.html5 import DateField
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/Student', methods=['GET', 'POST'])
def forstudnt():
    result = get_data(Student)
    form = Studform()
    if request.method == 'POST':
        print(form.gradebook_number.data)
        students = get_data_by_id(Student, form.gradebook_number.data)
        if students is not None:
            if form.gradebook_number.data == students.gradebook_number:
                students = Student(int(form.gradebook_number.data),form.full_name.data, form.stgroup.data, form.year_of_receipt.data.strftime('%Y-%m-%d'))
                update_data(students, Student)
            else:
                students = Student(form.gradebook_number.data, form.full_name.data, form.stgroup.data,form.year_of_receipt.data.strftime('%Y-%m-%d'))
                insert_data(students)
        else:
            students = Student(form.gradebook_number.data, form.full_name.data, form.stgroup.data,form.year_of_receipt.data.strftime('%Y-%m-%d'))
            insert_data(students)
        save()
        return redirect('/Student')
    return render_template('Student.html', students=result, form=form)


@app.route('/Student/delete/<gradebook_number>')
def user_delete(gradebook_number):
    delete_data(Student, gradebook_number)
    save()
    return redirect('/Student')


@app.route('/Student/edit/<gradebook_number>', methods=['GET'])
def student_edit(gradebook_number):
    if request.method == 'GET':
        students = get_data_by_id(Student, gradebook_number)
        result = get_data(Student)
        form = Studform()
        form.gradebook_number.data = students.gradebook_number
        form.full_name.data = students.full_name
        form.stgroup.data = students.stgroup
        form.year_of_receipt.data = students.year_of_receipt
        return render_template('Student.html', students=result, form=form)


@app.route('/Course_work', methods=['GET', 'POST'])
def forcoursework():
    result = get_data(CourseWork)
    form = CourseworkForm()
    if request.method == 'POST':
        print(form.initalization_num.data)
        works = get_data_by_init(CourseWork, form.initalization_num.data)
        if works is not None:
            if form.initalization_num.data == works.initalization_num:
                works = CourseWork(int(form.initalization_num.data),form.gradebook_number.data, form.cwname.data, form.research_direction.data, form.mark.data)
                update_data_cw(works, CourseWork)
            else:
                works = CourseWork(form.initalization_num.data,form.gradebook_number.data, form.cwname.data, form.research_direction.data, form.mark.data)
                insert_data(works)
        else:
            works = CourseWork(form.initalization_num.data,form.gradebook_number.data, form.cwname.data, form.research_direction.data, form.mark.data)
            insert_data(works)
        save()
        return redirect('/Course_work')
    return render_template('Course_work.html', works=result, form=form)


@app.route('/Course_work/delete/<initalization_num>')
def work_delete(initalization_num):
    delete_data_init(CourseWork, initalization_num)
    save()
    return redirect('/Course_work')


@app.route('/Course_work/edit/<initalization_num>', methods=['GET'])
def work_edit(initalization_num):
    if request.method == 'GET':
        works = get_data_by_init(CourseWork, initalization_num)
        result = get_data(CourseWork)
        form = CourseworkForm()
        form.initalization_num.data = works.initalization_num
        form.cwname.data = works.cwname
        form.gradebook_number.data = works.gradebook_number
        form.research_direction.data = works.research_direction
        form.mark.data = works.mark
        return render_template('Course_work.html', works=result, form=form)


@app.route('/Teacher', methods=['GET', 'POST'])
def forteacher():
    result = get_data(Teacher)
    form = TeacherForm()
    if request.method == 'POST':
        print(form.pass_number.data)
        teachers = get_data_by_pass(Teacher, form.pass_number.data)
        if teachers is not None:
            if form.pass_number.data == teachers.pass_number:
                teachers = Teacher(int(form.pass_number.data), form.full_name.data, form.department.data)
                update_data_t(teachers, Teacher)
            else:
                teachers = Teacher(form.pass_number.data, form.full_name.data, form.department.data)
                insert_data(teachers)
        else:
            teachers = Teacher(form.pass_number.data, form.full_name.data, form.department.data)
            insert_data(teachers)
        save()
        return redirect('/Teacher')
    return render_template('Teacher.html', teachers=result, form=form)


@app.route('/Teacher/delete/<pass_number>')
def teach_delete(pass_number):
    delete_data_pass(Teacher, pass_number)
    save()
    return redirect('/Teacher')


@app.route('/Teacher/edit/<pass_number>', methods=['GET'])
def teach_edit(pass_number):
    if request.method == 'GET':
        teachers = get_data_by_pass(Teacher, pass_number)
        result = get_data(Teacher)
        form = TeacherForm()
        form.pass_number.data = teachers.pass_number
        form.full_name.data = teachers.full_name
        form.department.data = teachers.department
        return render_template('Teacher.html', teachers=result, form=form)


@app.route('/Subjects', methods=['GET', 'POST'])
def forsubject():
    result = get_data(Subject)
    form = Subj_form()
    if request.method == 'POST':
        print(form.pass_num.data)
        subjects = get_data_by_passn(Subject, form.pass_num.data)
        if subjects is not None:
            if form.pass_num.data == subjects.pass_num:
                subjects = Subject(int(form.pass_num.data),form.sbname.data, form.student_rating.data, form.gradebook_number.data,form.pass_number.data)
                update_data_s(subjects, Subject)
            else:
                subjects = Subject(form.pass_num.data,form.sbname.data, form.student_rating.data, form.gradebook_number.data,form.pass_number.data)
                insert_data(subjects)
        else:
            subjects = Subject(form.pass_num.data,form.sbname.data, form.student_rating.data, form.gradebook_number.data,form.pass_number.data)
            insert_data(subjects)
        save()
        return redirect('/Subjects')
    return render_template('Subjects.html', subjects=result, form=form)


@app.route('/Subjects/delete/<pass_num>')
def subj_delete(pass_num):
    delete_data_passn(Subject, pass_num)
    save()
    return redirect('/Subjects')


@app.route('/Subjects/edit/<pass_num>', methods=['GET'])
def subj_edit(pass_num):
    if request.method == 'GET':
        subjects = get_data_by_passn(Subject, pass_num)
        result = get_data(Subject)
        form = Subj_form()
        form.pass_num.data = subjects.pass_num
        form.sbname.data = subjects.sbname
        form.student_rating.data = subjects.student_rating
        form.gradebook_number.data = subjects.gradebook_number
        form.pass_number.data = subjects.pass_number
        return render_template('Subjects.html', subjects=result, form=form)
		
		
		


def classificate(a,b,c):

    x_A = [[1, 1, 1],
           [2, 2, 2],
           [3, 3, 3]]
    x_B = [[4, 5, 5]]
    classes = ['A', 'B']

    sigma = 0.3
    input_data = [a, b, c]

    y3 = 0
    y4 = 0
    y3t = 0
    y4t = 0


    y1t = math.exp(-(((x_A[0][0] - input_data[0])**2 + (x_A[0][1] - input_data[1])**2 + (x_A[0][2] - input_data[2])**2)/(2 * (sigma**2)))) + math.exp(-(((x_A[1][0] - input_data[0])**2 + (x_A[1][1] - input_data[1])**2 + (x_A[1][2] - input_data[2])**2)/(2 * (sigma**2)))) + math.exp(-(((x_A[2][0] - input_data[0])**2 + (x_A[2][1] - input_data[1])**2 + (x_A[2][2] - input_data[2])**2)/(2 * (sigma**2))))
    y1 = y1t / len(x_A)
    y2t = math.exp(-(((x_B[0][0] - input_data[0])**2 + (x_B[0][1] - input_data[1])**2 + (x_B[0][2] - input_data[2])**2)/(2 * (sigma**2))))
    y2 = y2t / len(x_B)
    return[y1,y2]

		
            
@app.route('/Class', methods=['GET', 'POST'])
def forclass():
    form = Classform()
    if request.method == 'POST':
        print(form.gradebook_number.data)
        subjects = get_data_by(Subject, form.gradebook_number.data)
        marks = [sub.student_rating for sub in subjects]
        if subjects is not None:
            q = classificate(marks[0],marks[1],marks[2])
            if q[0] > q[1]:
                return render_template('Class.html', form=form, result='This student is at risk of flunk')
            else:
                return render_template('Class.html', form=form, result='This student is not at risk of flunk')
    return render_template('Class.html', form=form, result='')
