from flask import Flask, render_template, request, redirect, url_for

from dao.db import PostgresDb
from dao.orm.entities import *
from forms.discipline_form import DisciplineForm
from forms.student_form import StudentForm
from forms.teacher_form import TeacherForm
from forms.user_form import UserForm
from forms.task_form import TaskFrom
from forms.student_task_form import Student_TaskForm

import cluster
import json
import plotly
import plotly.graph_objs as go

app = Flask(__name__)
app.secret_key = 'development key'


class Login:
    name = ""
    password = ""
    isLogged = False
    isAdmin = False

    def Login(self, name, password, isAdmin=False):
        self.name = name
        self.password = password
        self.isLogged = True
        self.isAdmin = isAdmin


login = Login()


@app.route('/', methods=['GET', 'POST'])
def root():
    if login.isLogged:
        if login.isAdmin:
            return render_template('index.html')
        else:
            db = PostgresDb()

            user = db.sqlalchemy_session.query(Users).filter(Users.name == login.name,
                                                             Users.password == login.password).all()
            tasks = db.sqlalchemy_session.query(Student_Task).filter(Student_Task.student_name == user[0].name,
                                                                     Student_Task.student_group == user[0].sgroup).all()
            return render_template('Student_index.html', tasks = tasks)
    else:
        form = UserForm()
        if request.method == 'GET':
            return render_template('login_form.html', form=form, form_name="Login", action="")
        else:
            if not form.validate():
                return render_template('login_form.html', form=form, form_name="Login", action="")
            db = PostgresDb()
            # find professor

            user = db.sqlalchemy_session.query(Users).filter(Users.name == form.name.data,
                                                             Users.password == form.password.data).all()
            if user:
                login.Login(name=user[0].name, password=user[0].password)
                tasks = db.sqlalchemy_session.query(Student_Task).filter(Student_Task.student_name == user[0].name,
                                                    Student_Task.student_group == user[0].sgroup).all()
                return render_template('Student_index.html', tasks =tasks)
            elif form.name.data == 'admin' and form.password.data == 'admin':
                login.Login(name='admin', password='admin', isAdmin=True)
                return render_template('index.html')
            else:
                return render_template('login_form.html', form=form, form_name="Login", action="")

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():

    cluster_data = cluster.create_model()

    return render_template('analysis.html', clusters = cluster_data)


@app.route('/teacher', methods=['GET'])
def index_teacher():
    if login.isLogged:
        if login.isAdmin:
            db = PostgresDb()

            result = db.sqlalchemy_session.query(Teacher).all()

            return render_template('teacher.html', teachers=result)


@app.route('/new_teacher', methods=['GET', 'POST'])
def new_teacher():
    if login.isLogged:
        if login.isAdmin:
            form = TeacherForm()

            if request.method == 'POST':
                if not form.validate():
                    return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")
                else:
                    teacher_obj = Teacher(
                        name=form.name.data,
                        degree=form.degree.data
                    )
                    db = PostgresDb()
                    check = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == teacher_obj.name).all()
                    if check:
                        form.name.errors = ["Entity already exists"]
                        return render_template('teacher_form.html', form=form, form_name="New teacher",action="new_teacher")

                    db.sqlalchemy_session.add(teacher_obj)
                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_teacher'))

            return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")


@app.route('/edit_teacher', methods=['GET', 'POST'])
def edit_teacher():
    if login.isLogged:
        if login.isAdmin:
            form = TeacherForm()

            if request.method == 'GET':

                name = request.args.get('name')
                db = PostgresDb()
                teacher_obj = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == name).one()

                # fill form and send to user
                form.name.data = teacher_obj.name
                form.degree.data = teacher_obj.degree
                form.old_name.data = teacher_obj.name
                return render_template('teacher_form.html', form=form, form_name="Edit teacher", action="edit_teacher")

            else:
                if not form.validate():
                    return render_template('teacher_form.html', form=form, form_name="Edit teacher",
                                           action="edit_teacher")
                else:
                    db = PostgresDb()
                    # find professor

                    teacher_obj = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == form.old_name.data).one()

                    # update fields from form data
                    teacher_obj.name = form.name.data
                    teacher_obj.degree = form.degree.data

                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_teacher'))

@app.route('/delete_teacher')
def delete_teacher():
    if login.isLogged:
        if login.isAdmin:
            name = request.args.get('name')

            db = PostgresDb()

            result = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == name).one()

            db.sqlalchemy_session.delete(result)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_teacher'))

@app.route('/task', methods=['GET'])
def index_task():
    if login.isLogged:
        if login.isAdmin:
            db = PostgresDb()

            result = db.sqlalchemy_session.query(Task).all()

            return render_template('task.html', tasks=result)


@app.route('/new_task', methods=['GET', 'POST'])
def new_task():
    if login.isLogged:
        if login.isAdmin:
            form = TaskFrom()

            if request.method == 'POST':
                if not form.validate():
                    return render_template('task_form.html', form=form, form_name="New task", action="new_task")
                else:
                    db = PostgresDb()

                    tasks = db.sqlalchemy_session.query(Task).all()

                    task_obj = Task(
                        id = tasks[-1].id + 1,
                        name=form.name.data,
                        discipline_name=form.discipline_name.data,
                        value=form.value.data,
                        deadline=form.deadline.data
                    )
                    check = db.sqlalchemy_session.query(Task).filter(Task.name == task_obj.name,
                                                                     Task.discipline_name == task_obj.discipline_name,
                                                                     Task.deadline == task_obj.deadline).all()
                    if check:
                        form.name.errors = ["Entity already exists"]
                        return render_template('task_form.html', form=form, form_name="New task", action="new_task")

                    d = db.sqlalchemy_session.query(Discipline).filter(
                        Discipline.name == task_obj.discipline_name).all()
                    if not d:
                        form.discipline_name.errors = ["No discipline found"]
                        return render_template('task_form.html', form=form, form_name="New task", action="new_task")

                    db.sqlalchemy_session.add(task_obj)
                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_task'))

            return render_template('task_form.html', form=form, form_name="New task", action="new_task")


@app.route('/edit_task', methods=['GET', 'POST'])
def edit_task():
    if login.isLogged:
        if login.isAdmin:
            form = TaskFrom()

            if request.method == 'GET':

                name = request.args.get('name')
                db = PostgresDb()
                task_obj = db.sqlalchemy_session.query(Task).filter(Task.name == name).one()

                # fill form and send to user
                form.name.data = task_obj.name
                form.discipline_name.data = task_obj.discipline_name
                form.value.data = task_obj.value
                form.deadline.data = task_obj.deadline
                form.old_name.data = task_obj.name
                return render_template('task_form.html', form=form, form_name="Edit task", action="edit_task")

            else:
                if not form.validate():
                    return render_template('task_form.html', form=form, form_name="Edit task",
                                           action="edit_task")
                else:
                    db = PostgresDb()
                    # find professor

                    task_obj = db.sqlalchemy_session.query(Task).filter(Task.name == form.old_name.data).one()

                    d = db.sqlalchemy_session.query(Discipline).filter(Discipline.name == form.discipline_name.data).all()
                    if not d:
                        form.discipline_name.errors = ["No discipline found"]
                        return render_template('task_form.html', form=form, form_name="Edit task",action="edit_task")
                    # update fields from form data
                    task_obj.name = form.name.data
                    task_obj.discipline_name = form.discipline_name.data
                    task_obj.value = form.value.data
                    task_obj.deadline = form.deadline.data

                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_task'))

@app.route('/delete_task')
def delete_task():
    if login.isLogged:
        if login.isAdmin:
            name = request.args.get('name')

            db = PostgresDb()

            result = db.sqlalchemy_session.query(Task).filter(Task.name == name).one()

            db.sqlalchemy_session.delete(result)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_task'))

@app.route('/student_task', methods=['GET'])
def index_student_task():
    if login.isLogged:
        if login.isAdmin:
            db = PostgresDb()

            result = db.sqlalchemy_session.query(Student_Task).all()

            return render_template('student_task.html', tasks=result)


@app.route('/new_student_task', methods=['GET', 'POST'])
def new_student_task():
    if login.isLogged:
        if login.isAdmin:
            form = Student_TaskForm()

            if request.method == 'POST':
                if not form.validate():
                    return render_template('student_task_from.html', form=form, form_name="New student_task", action="new_student_task")
                else:
                    db = PostgresDb()

                    student_task_obj = Student_Task(
                        task_id = form.task_id.data,
                        student_name =form.student_name.data,
                        student_group =form.student_group.data
                    )
                    check = db.sqlalchemy_session.query(Student_Task).filter(Student_Task.task_id == student_task_obj.task_id,
                                                            Student_Task.student_name == student_task_obj.student_name,
                                                    Student_Task.student_group == student_task_obj.student_group).all()
                    if check:
                        form.name.errors = ["Entity already exists"]
                        return render_template('student_task_form.html', form=form, form_name="New student_task", action="new_student_task")

                    s = db.sqlalchemy_session.query(Student).filter(Student.name == student_task_obj.student_name,
                                                                    Student.sgroup == student_task_obj.student_group).all()
                    if not s:
                        form.student_name.errors = ["No student found"]
                        return render_template('student_task_form.html', form=form, form_name="New student_task", action="new_student_task")

                    t = db.sqlalchemy_session.query(Task).filter(Task.id == student_task_obj.task_id).all()
                    if not t:
                        form.task_id.errors = ["No tasks found"]
                        return render_template('student_task_form.html', form=form, form_name="New student_task", action="new_student_task")

                    db.sqlalchemy_session.add(student_task_obj)
                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_student_task'))

            return render_template('student_task_form.html', form=form, form_name="New student_task", action="new_student_task")


@app.route('/edit_student_task', methods=['GET', 'POST'])
def edit_student_task():
    if login.isLogged:
        if login.isAdmin:
            form = Student_TaskForm()

            if request.method == 'GET':

                id = request.args.get('id')
                s_name = request.args.get('s_name')
                s_group = request.args.get('s_group')
                db = PostgresDb()
                student_task_obj = db.sqlalchemy_session.query(Student_Task).filter(Student_Task.task_id == id,
                                                                                    Student_Task.student_name == s_name,
                                                                             Student_Task.student_group == s_group).one()

                # fill form and send to user
                form.task_id.data = student_task_obj.task_id
                form.student_name.data = student_task_obj.student_name
                form.student_group.data = student_task_obj.student_group
                form.old_id.data = student_task_obj.task_id
                form.old_name.data = student_task_obj.student_name
                form.old_group.data = student_task_obj.student_group

                return render_template('student_task_form.html', form=form, form_name="Edit student_task", action="edit_student_task")

            else:
                if not form.validate():
                    return render_template('student_task_form.html', form=form, form_name="Edit student_task",
                                           action="edit_student_task")
                else:
                    db = PostgresDb()
                    # find professor



                    student_task_obj = db.sqlalchemy_session.query(Student_Task).filter(Student_Task.task_id == form.old_id.data,
                                                                                    Student_Task.student_name == form.old_name.data,
                                                                                    Student_Task.student_group == form.old_group.data).one()

                    s = db.sqlalchemy_session.query(Student).filter(Student.name == form.old_name.data,
                                                                    Student.sgroup == form.old_group.data).all()
                    if not s:
                        form.student_name.errors = ["No student found"]
                        return render_template('student_task_form.html', form=form, form_name="Edit student_task",
                                               action="edit_student_task")

                    t = db.sqlalchemy_session.query(Task).filter(Task.id == form.old_id.data).all()
                    if not t:
                        form.task_id.errors = ["No tasks found"]
                        return render_template('student_task_form.html', form=form, form_name="Edit student_task",
                                               action="edit_student_task")

                    # update fields from form data
                    student_task_obj.task_id = form.task_id.data
                    student_task_obj.student_name = form.student_name.data
                    student_task_obj.student_group = form.student_group.data

                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_student_task'))

@app.route('/delete_student_task')
def delete_student_task():
    if login.isLogged:
        if login.isAdmin:
            id = request.args.get('id')
            s_name = request.args.get('s_name')
            s_group = request.args.get('s_group')

            db = PostgresDb()

            result = db.sqlalchemy_session.query(Student_Task).filter(Student_Task.task_id == id,
                                                                        Student_Task.student_name == s_name,
                                                                        Student_Task.student_group == s_group).one()

            db.sqlalchemy_session.delete(result)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student_task'))

@app.route('/student', methods=['GET'])
def index_student():
    if login.isLogged:
        if login.isAdmin:
            db = PostgresDb()

            result = db.sqlalchemy_session.query(Student).all()

            return render_template('student.html', students=result)


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    if login.isLogged:
        if login.isAdmin:
            form = StudentForm()

            if request.method == 'POST':
                if not form.validate():
                    return render_template('student_form.html', form=form, form_name="New student", action="new_student")
                else:
                    student_obj = Student(
                        name=form.name.data,
                        sgroup=form.group.data
                    )

                    db = PostgresDb()

                    check = db.sqlalchemy_session.query(Student).filter(Student.name== student_obj.name,
                                                                     Student.sgroup== student_obj.sgroup).all()
                    if check:
                        form.name.errors = ["Entity already exists"]
                        return render_template('student_form.html', form=form, form_name="New student", action="new_student")

                    db.sqlalchemy_session.add(student_obj)
                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_student'))

            return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    if login.isLogged:
        if login.isAdmin:
            form = StudentForm()

            if request.method == 'GET':

                name, group = request.args.get('name'), int(request.args.get('group'))
                db = PostgresDb()
                student = db.sqlalchemy_session.query(Student).filter(Student.name == name, Student.sgroup == group).one()

                # fill form and send to student
                form.name.data = student.name
                form.group.data = student.sgroup
                form.old_name.data = student.name
                form.old_group.data = student.sgroup
                return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")

            else:

                if not form.validate():
                    return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")
                else:
                    db = PostgresDb()
                    # find student
                    student = db.sqlalchemy_session.query(Student).filter(Student.name == form.old_name.data,
                                                                          Student.sgroup == form.old_group.data).one()

                    # update fields from form data
                    student.name = form.name.data
                    student.sgroup = form.group.data

                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_student'))


@app.route('/delete_student')
def delete_student():
    if login.isLogged:
        if login.isAdmin:
            name, group = request.args.get('name'), int(request.args.get('group'))

            db = PostgresDb()

            result = db.sqlalchemy_session.query(Student).filter(Student.name == name, Student.sgroup == group).one()

            db.sqlalchemy_session.delete(result)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student'))


@app.route('/discipline', methods=['GET'])
def index_discipline():
    if login.isLogged:
        if login.isAdmin:
            db = PostgresDb()

            discipline = db.sqlalchemy_session.query(Discipline).all()

            return render_template('discipline.html', disciplines=discipline)


@app.route('/new_discipline', methods=['GET', 'POST'])
def new_discipline():
    if login.isLogged:
        if login.isAdmin:
            form = DisciplineForm()

            if request.method == 'POST':
                if not form.validate():
                    return render_template('discipline_form.html', form=form, form_name="New discipline",
                                           action="new_discipline")
                else:
                    discipline_obj = Discipline(
                        name=form.name.data,
                        teacher_name=form.teacher_name.data
                    )

                    db = PostgresDb()
                    check = db.sqlalchemy_session.query(Discipline).filter(Discipline.name== discipline_obj.name,
                                                                        Discipline.teacher_name== discipline_obj.teacher_name).all()
                    if check:
                        form.name.errors = ["Entity already exists"]
                        return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")

                    a = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == form.teacher_name.data).all()
                    if not a:
                        form.teacher_name.errors = ["No teacher found"]
                        return render_template('discipline_form.html', form=form, form_name="New discipline",
                                               action="new_discipline")
                    db.sqlalchemy_session.add(discipline_obj)
                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_discipline'))

            return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")


@app.route('/edit_discipline', methods=['GET', 'POST'])
def edit_discipline():
    if login.isLogged:
        if login.isAdmin:
            form = DisciplineForm()

            if request.method == 'GET':
                name = request.args.get('name')

                db = PostgresDb()

                # -------------------------------------------------------------------- filter for "and" google
                discipline = db.sqlalchemy_session.query(Discipline).filter(
                    Discipline.name == name).one()

                a = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == discipline.teacher_name).all()
                if not a:
                    return render_template('discipline_form.html', form=form, form_name="Edit discipline",
                                           action="edit_discipline")
                # fill form and send to discipline
                form.teacher_name.data = discipline.teacher_name
                form.name.data = discipline.name
                form.old_name.data = discipline.name
                return render_template('discipline_form.html', form=form, form_name="Edit discipline", action="edit_discipline")

            else:

                if not form.validate():
                    return render_template('discipline_form.html', form=form, form_name="Edit discipline",
                                           action="edit_discipline")
                else:
                    db = PostgresDb()
                    # find discipline
                    discipline = db.sqlalchemy_session.query(Discipline).filter(Discipline.name == form.old_name.data).one()

                    a = db.sqlalchemy_session.query(Teacher).filter(Teacher.name == form.teacher_name.data).all()
                    if not a:
                        form.teacher_name.errors = ["No teacher found"]
                        return render_template('discipline_form.html', form=form, form_name="Edit discipline",
                                           action="edit_discipline")
                    # update fields from form data
                    discipline.name = form.name.data
                    discipline.teacher_name = form.teacher_name.data

                    db.sqlalchemy_session.commit()

                    return redirect(url_for('index_discipline'))


@app.route('/delete_discipline')
def delete_discipline():
    if login.isLogged:
        if login.isAdmin:
            name = request.args.get('name')
            db = PostgresDb()

            result = db.sqlalchemy_session.query(Discipline).filter(
                Discipline.name == name).one()

            db.sqlalchemy_session.delete(result)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_discipline'))


if __name__ == '__main__':
    app.run(debug=True)
