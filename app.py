from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date

from source.analysis import cluster
from source.analysis import regression
from source.dao.orm.populate import populate
from source.dao.db import PostgresDb
from source.dao.data import *
from source.dao.orm.entities import *
from source.forms.record_form import RecordBook
from source.forms.record_search_form import RecordSearchForm
from source.forms.admin_form import AdminForm
from source.forms.student_form import StudentForm
from source.forms.professor_form import ProfessorForm
from source.forms.discipline_form import DisciplineForm
from source.forms.search_student_form import StudentSearchForm
from source.forms.search_student_record_from import StudentSearchRecordForm

import json
import plotly
import plotly.graph_objs as go
import os

app = Flask(__name__)

populate_flag = False

app.secret_key = os.getenv("SECRET_KEY", "jkm-vsnej9l-vm9sqm3:lmve")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  "postgresql://{}:{}@{}:{}/{}".format(username, password, host, port,
                                                                                       database))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def check(admin_page):
    if not session["log_in"] or (admin_page and not session["admin"]) or (not admin_page and session["admin"]):
        return 1
    else:
        return 0


@app.route('/cluster_update')
def cluster_update():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    try:
        cluster.create_model(source_path="source/analysis/")
        return render_template('index.html', message="cluster update done")
    except Exception as e:
        return render_template('index.html', message="cluster update error: {}".format(e))


@app.route('/regression_update')
def regression_update():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    try:
        regression.create_model(source_path="source/analysis/")
        return render_template('index.html', message="regression update done")
    except Exception as e:
        return render_template('index.html', message="regression update error: {}".format(e))


@app.route('/populate_my_db_by_function')
def populate_db():
    global populate_flag
    if check(admin_page=True) and populate_flag is not True:
        return render_template('login.html', error="no rights, login another way")

    try:
        populate(path="source/dao/orm/")
        populate_flag = True
        return render_template('index.html', message="populate done")
    except:
        return render_template('index.html', message="populate error")


@app.route('/')
def hello():
    return render_template('login.html', error=False)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('log_in', None)
    session.pop('admin', None)
    session.pop('student_id', None)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = PostgresDb()

        login = request.form['login']
        password = request.form['password']
        admin = db.sqlalchemy_session.query(Admin).filter(Admin.login == login, Admin.password == password).all()

        if admin:

            session['admin'] = True
            session['log_in'] = True

            return redirect(url_for('index'))
        else:
            student = db.sqlalchemy_session.query(Student).filter(Student.login == login,
                                                                  Student.password == password).all()
            if student:

                if len(student) > 1:
                    raise Exception('more than 2 students have same login')
                if student[0].student_date_expelled is not None:
                    return render_template('login.html', error="user has been deleted")

                session['admin'] = False
                session['log_in'] = True

                session['student_id'] = student[0].student_id
                return redirect(url_for('record_book_index'))
            else:

                session['admin'] = False
                session['log_in'] = False

                return render_template('login.html', error="Wrong login or password")
    return render_template('login.html', error=False)


# RECORD BOOK --------------------------------------------------------------------------------------------------------

@app.route('/record_book_index')
def record_book_index():
    if check(admin_page=False):
        return render_template('login.html', error="no rights, login another way")

    db = PostgresDb()
    student_id = session["student_id"]
    student = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()

    return render_template('index_student.html', uni=student.student_university, faculty=student.student_faculty,
                           group=student.student_group, name=student.name, surname=student.surname)


@app.route('/record_book', methods=["POST", "GET"])
def record_book():
    if check(admin_page=False):
        return render_template('login.html', error="no rights, login another way")

    db = PostgresDb()
    student_id = session["student_id"]
    student_records = db.sqlalchemy_session.query(StudentRecordBook).filter(
        StudentRecordBook.student_id_fk == student_id).order_by(StudentRecordBook.exam_passed).all()

    dates = []
    for date_s in student_records:
        if date(int(date_s.exam_passed.year), 9, 1) < date_s.exam_passed or \
                date_s.exam_passed < date(int(date_s.exam_passed.year), 1, 31):
            if date_s.exam_passed.year not in dates:
                dates.append(date_s.exam_passed.year)

    if not dates:
        dates = [2019]

    year, semester = request.args.get('year'), request.args.get('semester')

    if request.method == "POST":
        record_form = RecordSearchForm(dates)
    elif year and semester:
        record_form = RecordSearchForm(dates, year=year, semester=semester)
    else:
        record_form = RecordSearchForm(dates, year=dates[-1], semester=1)
    records = record_form.search(student_id)

    return render_template('record_student.html', records=records, record_form=record_form,
                           year="{}-{}".format(int(record_form.year.data), int(record_form.year.data) + 1),
                           semester=record_form.semester.data)


@app.route('/new_record', methods=['GET', 'POST'])
def new_record():
    if check(admin_page=False):
        return render_template('login.html', error="no rights, login another way")

    db = PostgresDb()
    student = db.sqlalchemy_session.query(Student).filter(Student.student_id == session["student_id"]).one()

    form = RecordBook(uni=student.student_university, faculty=student.student_faculty)
    student_id = session["student_id"]
    if request.method == 'POST':
        if not form.validate():
            return render_template('record_form.html', form=form, form_name="New record", action="new_record")
        else:

            record_obj = StudentRecordBook(
                student_id_fk=student_id,
                discipline_id_fk=form.discipline_chose.data,
                professor_id_fk=form.professor_chose.data,
                semester_mark=form.semester_mark.data,
                final_mark=form.final_mark.data,
                exam_passed=form.exam_passed.data
            )

            db.sqlalchemy_session.add(record_obj)
            db.sqlalchemy_session.commit()

            semester = 2 if 1 < form.exam_passed.data.month < 9 else 1
            year = form.exam_passed.data.year if \
                semester == 1 and form.exam_passed.data.month != 1 else form.exam_passed.data.year - 1

            # todo add transferring data about semester and year
            return redirect(url_for('record_book', semester=semester, year=year))

    return render_template('record_form.html', form=form, form_name="New record", action="new_record")


@app.route('/edit_record', methods=['GET', 'POST'])
def edit_record():
    if check(admin_page=False):
        return render_template('login.html', error="no rights, login another way")

    student_id = session["student_id"]

    db = PostgresDb()
    student = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()
    uni, faculty = student.student_university, student.student_faculty

    if request.method == 'GET':

        professor_id = request.args.get('professor_id')
        discipline_id = request.args.get('discipline_id')
        form = RecordBook(uni=uni, faculty=faculty, professor_chose=professor_id, discipline_chose=discipline_id)

        db = PostgresDb()
        record = db.sqlalchemy_session.query(StudentRecordBook). \
            filter(StudentRecordBook.student_id_fk == student_id,
                   StudentRecordBook.discipline_id_fk == discipline_id).one()

        # fill form and send to student
        form.discipline_id.data = record.discipline_id_fk
        form.professor_id.data = record.professor_id_fk
        form.semester_mark.data = record.semester_mark
        form.final_mark.data = record.final_mark
        form.exam_passed.data = record.exam_passed

        return render_template('record_form.html', form=form, form_name="Edit record", action="edit_record")

    else:
        form = RecordBook(uni=uni, faculty=faculty)
        if not form.validate():
            return render_template('record_form.html', form=form, form_name="Edit record", action="edit_record")
        else:
            db = PostgresDb()
            # find record
            if int(form.discipline_id.data) != form.discipline_chose.data:
                # if we change PK of entity we have to check existing of this record at db
                record = db.sqlalchemy_session.query(StudentRecordBook). \
                    filter(StudentRecordBook.student_id_fk == student_id,
                           StudentRecordBook.discipline_id_fk == form.discipline_chose.data).all()

                record_old_obj = db.sqlalchemy_session.query(StudentRecordBook). \
                    filter(StudentRecordBook.student_id_fk == student_id,
                           StudentRecordBook.discipline_id_fk == int(form.discipline_id.data)).one()

                db = PostgresDb()
                if record:
                    # if such record exist lets change it and delete "edited record"

                    record = record[0]
                    record.professor_id_fk = form.professor_chose.data
                    record.semester_mark = form.semester_mark.data
                    record.final_mark = form.final_mark.data
                    record.exam_passed = form.exam_passed.data
                else:
                    # if such record doesnt exist lets create it and delete "edited record"

                    record_new_obj = StudentRecordBook(
                        student_id_fk=student_id,
                        discipline_id_fk=form.discipline_chose.data,
                        professor_id_fk=form.professor_chose.data,
                        semester_mark=form.semester_mark,
                        final_mark=form.final_mark,
                        exam_passed=form.exam_passed
                    )
                    db.sqlalchemy_session.add(record_new_obj)

                db.sqlalchemy_session.delete(record_old_obj)

            else:
                # if we dont change PK of entity we just change fields

                record = db.sqlalchemy_session.query(StudentRecordBook). \
                    filter(StudentRecordBook.student_id_fk == student_id,
                           StudentRecordBook.discipline_id_fk == form.discipline_chose.data).one()

                # update fields from form data
                record.professor_id_fk = form.professor_chose.data
                record.semester_mark = form.semester_mark.data
                record.final_mark = form.final_mark.data
                record.exam_passed = form.exam_passed.data

            db.sqlalchemy_session.commit()

            semester = 2 if 1 < form.exam_passed.data.month < 9 else 1
            year = form.exam_passed.data.year if \
                semester == 1 and form.exam_passed.data.month != 1 else form.exam_passed.data.year - 1
            return redirect(url_for('record_book', semester=semester, year=year))


@app.route('/delete_record')
def delete_record():
    if check(admin_page=False):
        return render_template('login.html', error="no rights, login another way")

    student_id = session["student_id"]
    discipline_id = request.args.get('discipline_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(StudentRecordBook).filter(
        StudentRecordBook.discipline_id_fk == discipline_id,
        StudentRecordBook.student_id_fk == student_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('record_book'))


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if check(admin_page=False):
        return render_template('login.html', error="no rights, login another way")

    data = {}

    cluster_data = cluster.get_cluster_val(student_id=session["student_id"])

    scatter_1 = go.Scatter(
        x=[i[0] for i in cluster_data[2]], y=[i[1] for i in cluster_data[2]],
        name='good student',
        mode='markers',
        marker_color='rgba(152, 0, 0, .8)'
    )
    scatter_2 = go.Scatter(
        x=[i[0] for i in cluster_data[3]], y=[i[1] for i in cluster_data[3]],
        name='not good students',
        mode='markers',
        marker_color='rgba(0,0,0,1)'
    )
    scatter_3 = go.Scatter(
        x=cluster_data[0], y=cluster_data[1],
        name='centers',
        mode='markers',
        marker={"symbol": "star-triangle-down-open"},
        marker_color='rgba(21,140,0,1)'
    )

    data["scatter_all_cluster"] = [scatter_1, scatter_2, scatter_3]
    json_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    db = PostgresDb()
    student = db.sqlalchemy_session.query(Student).filter(Student.student_id == session["student_id"]).one()
    uni, faculty = student.student_university, student.student_faculty

    form = RecordBook(uni=uni, faculty=faculty)
    delattr(form, "final_mark")
    delattr(form, "exam_passed")

    if request.method == "POST":
        if not form.validate():
            return render_template('analysis.html', form=form, json=json_data, predicted_cluster=cluster_data[-1],
                                   predicted_mark=0)
        predict = regression.get_regression_val(semester_val=form.semester_mark.data,
                                                discipline_id=form.discipline_chose.data,
                                                professor_id=form.professor_chose.data)
        return render_template('analysis.html', json=json_data, predicted_cluster=cluster_data[-1], form=form,
                               predicted_mark=int(predict))

    return render_template('analysis.html', json=json_data, predicted_cluster=cluster_data[-1], form=form,
                           predicted_mark=0)


# ADMIN  -------------------------------------------------------------------------------------------------------------


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    pie_labels = []
    data = {}

    # pie plot -------------------------------------------------------------------------------------------------------
    student_form = StudentSearchForm()
    student_form.init()

    for query, label in zip(*student_form.search(method=request.method)):

        if not query:
            continue

        groups, counts = zip(*query)
        pie = go.Pie(
            labels=['group = {}'.format(group) for group in groups],
            values=counts
        )
        data[label] = [pie]
        pie_labels.append(label)

    # scatter plot ---------------------------------------------------------------------------------------------------
    record_book_form = StudentSearchRecordForm()
    record_book_form.init()

    return_val = record_book_form.search(method=request.method)
    if return_val:
        semester, final = zip(*return_val)
        bar = go.Scatter(
            x=semester,
            y=final,
            mode='markers'
        )

        data["bar"] = [bar]

    json_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', json=json_data, pie_labels=pie_labels, student_form=student_form,
                           record_book_form=record_book_form)


# PROFESSOR ORIENTED QUERIES ------------------------------------------------------------------------------------------


@app.route('/professor', methods=['GET'])
def index_professor():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    db = PostgresDb()

    deleted = request.args.get('deleted')

    if deleted:
        result = db.sqlalchemy_session.query(Professor).all()
    else:
        deleted = False
        result = db.sqlalchemy_session.query(Professor).filter(Professor.professor_date_expelled == None).all()

    return render_template('professor.html', professors=result, deleted=deleted)


@app.route('/new_professor', methods=['GET', 'POST'])
def new_professor():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    form = ProfessorForm()

    if request.method == 'POST':
        form.strip()
        if not form.validate():
            return render_template('professor_form.html', form=form, form_name="New professor", action="new_professor")
        else:
            db = PostgresDb()

            if db.sqlalchemy_session.query(Professor).filter(
                    Professor.professor_university == form.professor_university.data,
                    Professor.professor_department == form.professor_department.data,
                    Professor.name == form.professor_name.data,
                    Professor.surname == form.professor_surname.data).all():
                return render_template('professor_form.html', form=form, form_name="New professor",
                                       action="new_professor",
                                       msg="Cant add this record. Use another combination of {professor_university, "
                                           "professor_department, name, surname}")
            professor_obj = Professor(
                professor_university=form.professor_university.data,
                professor_department=form.professor_department.data,
                name=form.professor_name.data,
                surname=form.professor_surname.data,
                professor_date_enrollment=form.professor_date_enrollment.data.strftime("%d-%b-%y"),
                professor_degree=form.professor_degree.data)

            db.sqlalchemy_session.add(professor_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_professor'))

    return render_template('professor_form.html', form=form, form_name="New professor", action="new_professor")


@app.route('/edit_professor', methods=['GET', 'POST'])
def edit_professor():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    form = ProfessorForm()

    if request.method == 'GET':

        professor_id = request.args.get('professor_id')
        db = PostgresDb()
        professor_obj = db.sqlalchemy_session.query(Professor).filter(Professor.professor_id == professor_id).one()

        # fill form and send to user
        form.professor_id.data = professor_obj.professor_id
        form.professor_university.data = professor_obj.professor_university
        form.professor_department.data = professor_obj.professor_department
        form.professor_name.data = professor_obj.name
        form.professor_surname.data = professor_obj.surname
        form.professor_date_enrollment.data = professor_obj.professor_date_enrollment
        form.professor_degree.data = professor_obj.professor_degree

        return render_template('professor_form.html', form=form, form_name="Edit professor", action="edit_professor")

    else:
        form.strip()

        if not form.validate():
            return render_template('professor_form.html', form=form, form_name="Edit professor",
                                   action="edit_professor")
        else:
            db = PostgresDb()

            if db.sqlalchemy_session.query(Professor).filter(
                    Professor.professor_university == form.professor_university.data,
                    Professor.professor_department == form.professor_department.data,
                    Professor.name == form.professor_name.data,
                    Professor.surname == form.professor_surname.data,
                    Professor.professor_id == form.professor_id.data).all():
                return render_template('professor_form.html', form=form, form_name="Edit professor",
                                       action="edit_professor",
                                       msg="Cant edit this record. Use another combination of {professor_university, "
                                           "professor_department, name, surname}")
            # find professor
            professor_obj = db.sqlalchemy_session.query(Professor).filter(Professor.professor_id ==
                                                                          form.professor_id.data).one()

            # update fields from form data
            professor_obj.professor_id = form.professor_id.data
            professor_obj.professor_university = form.professor_university.data
            professor_obj.professor_department = form.professor_department.data
            professor_obj.name = form.professor_name.data
            professor_obj.surname = form.professor_surname.data
            professor_obj.professor_date_enrollment = form.professor_date_enrollment.data.strftime("%d-%b-%y")
            professor_obj.professor_degree = form.professor_degree.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_professor'))


@app.route('/delete_professor')
def delete_professor():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    professor_id = request.args.get('professor_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Professor).filter(Professor.professor_id == professor_id).one()

    result.professor_date_expelled = date.today()
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_professor'))


# END PROFESSOR ORIENTED QUERIES --------------------------------------------------------------------------------------

# STUDENT ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/student', methods=['GET'])
def index_student():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    db = PostgresDb()

    deleted = request.args.get('deleted')

    if deleted:
        result = db.sqlalchemy_session.query(Student).all()
    else:
        deleted = False
        result = db.sqlalchemy_session.query(Student).filter(Student.student_date_expelled == None).all()

    return render_template('student.html', students=result, deleted=deleted)


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    form = StudentForm()

    if request.method == 'POST':
        form.strip()
        if not form.validate():
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            db = PostgresDb()
            if db.sqlalchemy_session.query(Student).filter(Student.login == form.student_login.data).all():
                return render_template('student_form.html', form=form, form_name="New student", action="new_student",
                                       msg="Cant add this record. Use another login name")
            if db.sqlalchemy_session.query(Student).filter(Student.student_university == form.student_university.data,
                                                           Student.student_faculty == form.student_faculty.data,
                                                           Student.student_group == form.student_group.data,
                                                           Student.name == form.student_name.data,
                                                           Student.surname == form.student_surname.data).all():
                return render_template('student_form.html', form=form, form_name="New student", action="new_student",
                                       msg="Cant add this record. Use another combination of {student_university, "
                                           "student_faculty, student_group, name, surname}")

            student_obj = Student(
                login=form.student_login.data,
                password=form.student_password.data,
                student_university=form.student_university.data,
                student_faculty=form.student_faculty.data,
                student_group=form.student_group.data,
                name=form.student_name.data,
                surname=form.student_surname.data,
                student_date_enrollment=form.student_date_enrollment.data.strftime("%d-%b-%y"))

            db.sqlalchemy_session.add(student_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    form = StudentForm()

    if request.method == 'GET':

        student_id = request.args.get('student_id')
        db = PostgresDb()
        student = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()

        # fill form and send to student
        form.student_id.data = student.student_id
        form.student_login.data = student.login
        form.student_password.data = student.password
        form.student_name.data = student.name
        form.student_surname.data = student.surname
        form.student_group.data = student.student_group
        form.student_university.data = student.student_university
        form.student_faculty.data = student.student_faculty
        form.student_date_enrollment.data = student.student_date_enrollment

        return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")

    else:
        form.strip()
        if not form.validate():
            return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")
        else:
            db = PostgresDb()
            if db.sqlalchemy_session.query(Student).filter(Student.login == form.student_login.data,
                                                           Student.student_id != form.student_id.data).all():
                return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student",
                                       msg="Cant edit this record. Use another login name")

            if db.sqlalchemy_session.query(Student).filter(Student.student_university == form.student_university.data,
                                                           Student.student_faculty == form.student_faculty.data,
                                                           Student.student_group == form.student_group.data,
                                                           Student.name == form.student_name.data,
                                                           Student.surname == form.student_surname.data,
                                                           Student.student_id != form.student_id.data).all():
                return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student",
                                       msg="Cant edit this record. Use another combination of {student_university, "
                                           "student_faculty, student_group, name, surname}")
            # find student
            student = db.sqlalchemy_session.query(Student).filter(Student.student_id == form.student_id.data).one()

            # update fields from form data
            student.student_id = form.student_id.data
            student.login = form.student_login.data
            student.password = form.student_password.data
            student.student_university = form.student_university.data
            student.student_faculty = form.student_faculty.data
            student.student_group = form.student_group.data
            student.name = form.student_name.data
            student.surname = form.student_surname.data
            student.student_date_enrollment = form.student_date_enrollment.data.strftime("%d-%b-%y")

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student'))


@app.route('/delete_student')
def delete_student():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    student_id = request.args.get('student_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()
    result.student_date_expelled = date.today()

    db.sqlalchemy_session.commit()

    return redirect(url_for('index_student'))


# END STUDENT ORIENTED QUERIES ----------------------------------------------------------------------------------------

# ADMIN ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/admin', methods=['GET'])
def index_admin():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Admin).all()

    return render_template('admin.html', admins=result)


@app.route('/new_admin', methods=['GET', 'POST'])
def new_admin():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    form = AdminForm()
    if request.method == 'POST':
        form.strip()
        if not form.validate():
            return render_template('admin_form.html', form=form, form_name="New admin", action="new_admin")
        else:
            admin_obj = Admin(
                login=form.login.data,
                password=form.password.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(admin_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_admin'))

    return render_template('admin_form.html', form=form, form_name="New admin", action="new_admin")


@app.route('/edit_admin', methods=['GET', 'POST'])
def edit_admin():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    form = AdminForm()

    if request.method == 'GET':

        admin_id = request.args.get('admin_id')
        db = PostgresDb()
        admin = db.sqlalchemy_session.query(Admin).filter(Admin.id == admin_id).one()

        # fill form and send to student
        form.id.data = admin.id
        form.login.data = admin.login
        form.password.data = admin.password

        return render_template('admin_form.html', form=form, form_name="Edit admin", action="edit_admint")

    else:
        form.strip()
        if not form.validate():
            return render_template('admin_form.html', form=form, form_name="Edit admin", action="edit_admin")
        else:
            db = PostgresDb()
            # find student
            admin = db.sqlalchemy_session.query(Admin).filter(Admin.id == form.id.data).one()

            # update fields from form data
            admin.id = form.id.data
            admin.login = form.login.data
            admin.password = form.password.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_admin'))


@app.route('/delete_admin')
def delete_admin():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    admin_id = request.args.get('admin_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Admin).filter(Admin.id == admin_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_admin'))


# END ADMIN ORIENTED QUERIES ----------------------------------------------------------------------------------------

# DISCIPLINE ORIENTED QUERIES ---------------------------------------------------------------------------------------

@app.route('/discipline', methods=['GET'])
def index_discipline():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    db = PostgresDb()

    discipline = db.sqlalchemy_session.query(Discipline).all()

    if request.args.get("msg"):
        return render_template('discipline.html', disciplines=discipline, msg_error=str(request.args.get("msg")))
    else:
        return render_template('discipline.html', disciplines=discipline, msg_error=0)


@app.route('/new_discipline', methods=['GET', 'POST'])
def new_discipline():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    form = DisciplineForm()
    if request.method == 'POST':
        form.strip()
        if not form.validate():
            return render_template('discipline_form.html', form=form, form_name="New discipline",
                                   action="new_discipline")
        else:
            discipline_obj = Discipline(
                discipline_university=form.discipline_university.data,
                discipline_faculty=form.discipline_faculty.data,
                discipline_name=form.discipline_name.data,
                discipline_exam=form.discipline_exam.data,
                discipline_hours_for_semester=form.discipline_hours_for_semester.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(discipline_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_discipline'))

    return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")


@app.route('/edit_discipline', methods=['GET', 'POST'])
def edit_discipline():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    form = DisciplineForm()

    if request.method == 'GET':

        discipline_id = request.args.get('discipline_id')
        db = PostgresDb()

        discipline = db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == discipline_id).one()

        # fill form and send to discipline
        form.discipline_id.data = discipline_id
        form.discipline_university.data = discipline.discipline_university
        form.discipline_faculty.data = discipline.discipline_faculty
        form.discipline_name.data = discipline.discipline_name
        form.discipline_exam.data = discipline.discipline_exam
        form.discipline_hours_for_semester.data = discipline.discipline_hours_for_semester

        return render_template('discipline_form.html', form=form, form_name="Edit discipline", action="edit_discipline")

    else:
        form.strip()
        if not form.validate():
            return render_template('discipline_form.html', form=form, form_name="Edit discipline",
                                   action="edit_discipline")
        else:
            db = PostgresDb()
            # find discipline
            discipline = db.sqlalchemy_session.query(Discipline).filter(
                Discipline.discipline_id == int(form.discipline_id.data)).one()

            # update fields from form data
            discipline.discipline_university = form.discipline_university.data
            discipline.discipline_faculty = form.discipline_faculty.data
            discipline.discipline_name = form.discipline_name.data
            discipline.discipline_exam = form.discipline_exam.data
            discipline.discipline_hours_for_semester = form.discipline_hours_for_semester.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_discipline'))


@app.route('/delete_discipline')
def delete_discipline():
    if check(admin_page=True):
        return render_template('login.html', error="no rights, login another way")

    discipline_id = request.args.get('discipline_id')

    db = PostgresDb()

    if db.sqlalchemy_session.query(StudentRecordBook).filter(StudentRecordBook.discipline_id_fk == discipline_id).all():
        return redirect(url_for('index_discipline', msg="Cant delete this record. Use this record "
                                                        "at other important entity"))

    result = db.sqlalchemy_session.query(Discipline).filter(
        Discipline.discipline_id == discipline_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_discipline'))


# END DISCIPLINE ORIENTED QUERIES -----------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
