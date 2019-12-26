from flask import Flask, flash, render_template, request, redirect, url_for
import sqlalchemy.sql as sql
from sqlalchemy import func
from dao.orm.entities import *
from dao.db import PostgresDb
from forms.apply_form import ApplyForm
from forms.teacher_form import TeacherForm
from forms.group_form import GroupForm
from forms.subject_form import SubjectForm
from forms.scedule_form import SceduleForm
from forms.search_group_form import GroupSearchForm
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

    def Login(self,name,password, isAdmin= False):
        self.name = name
        self.password = password
        self.isLogged = True
        self.isAdmin = isAdmin


log = Login()

@app.route('/', methods=['GET', 'POST'])
def root():
    if log.isLogged:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    db = PostgresDb()
    group_form = GroupSearchForm()
    group_form.init()

    pie_labels = []
    data = {
        "bar": []
    }

    for query, label in zip(*group_form.search(method=request.method)):

        if not query:
            continue

        groups, counts = zip(*query)
        pie = go.Pie(
            labels=[f'group = {group}' for group in groups],
            values=counts
        )
        data[label] = [pie]
        pie_labels.append(label)

    points = db.sqlalchemy_session.query(Subject.subj_name, Subject.subj_hours).distinct(
        Subject.subj_name, Subject.subj_hours).filter(Subject.subj_name != '').all()

    semester, final = zip(*points)
    bar = go.Scatter(
        x=semester,
        y=final,
        mode='markers'
    )

    data["bar"].append(bar)
    json_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', json=json_data, pie_labels=pie_labels, group_form=group_form)


@app.route('/teacher', methods=['GET'])
def index_teacher():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Teacher).all()

    return render_template('teacher.html', teachers=result)


@app.route('/new_teacher', methods=['GET', 'POST'])
def new_teacher():
    form = TeacherForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('teacher_form.html', form=form, action="new_teacher")
        else:
            # db = PostgresDb()
            teacher_obj = Teacher(
                teach_name=form.teacher_name.data,
                teach_faculty=form.teacher_faculty.data)

            # check = db.sqlalchemy_session.query(Teacher).filter(Teacher.teach_name == teacher_obj.teach_name,
            #                                                     Teacher.teach_faculty == teacher_obj.teach_faculty)
            # if check:
            #     TeacherForm.errors = ["Entity already exists"]
            #     return render_template('teacher_form.html', form=form, action="new_teacher")
            db = PostgresDb()
            db.sqlalchemy_session.add(teacher_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_teacher'))

    return render_template('teacher_form.html', form=form, action="new_teacher")


@app.route('/edit_teacher', methods=['GET', 'POST'])
def edit_teacher():
    form = TeacherForm()

    if request.method == 'GET':

        teacher_id = request.args.get('teacher_id')
        db = PostgresDb()
        teacher_obj = db.sqlalchemy_session.query(Teacher).filter(Teacher.teacher_id == teacher_id).one()

        # fill form and send to user
        form.teacher_id.data = teacher_obj.teacher_id
        form.teacher_faculty.data = teacher_obj.teach_faculty
        form.teacher_name.data = teacher_obj.teach_name

        return render_template('teacher_form.html', form=form, form_name="Edit teacher", action="edit_teacher")

    else:
        if not form.validate():
            return render_template('teacher_form.html', form=form, form_name="Edit teacher",
                                   action="edit_teacher")
        else:
            db = PostgresDb()
            # find professor
            teacher_obj = db.sqlalchemy_session.query(Teacher).filter(Teacher.teacher_id ==
                                                                          form.teacher_id.data).one()

            # update fields from form data
            teacher_obj.teacher_id = form.teacher_id.data
            teacher_obj.teach_faculty = form.teacher_faculty.data
            teacher_obj.teach_name = form.teacher_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_teacher'))


@app.route('/delete_teacher')
def delete_teacher():
    teacher_id = request.args.get('teacher_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Teacher).filter(Teacher.teacher_id == teacher_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_teacher'))


# END PROFESSOR ORIENTED QUERIES --------------------------------------------------------------------------------------

# STUDENT ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/group', methods=['GET'])
def index_group():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Group).all()

    return render_template('group.html', groups=result)


@app.route('/new_group', methods=['GET', 'POST'])
def new_group():
    form = GroupForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('group_form.html', form=form, form_name="New group", action="new_group")
        else:
            # db = PostgresDb()
            group_obj = Group(
                group_faculty=form.group_faculty.data,
                group_name=form.group_name.data)
            # check = db.sqlalchemy_session.query(Group).filter(Group.group_name == group_obj.group_name,
            #                                                     Group.group_faculty == group_obj.group_faculty)
            # if check:
            #     TeacherForm.errors = ["Entity already exists"]
            #     return render_template('group_form.html', form=form, action="new_group")
            db = PostgresDb()
            db.sqlalchemy_session.add(group_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_group'))

    return render_template('group_form.html', form=form, form_name="New group", action="new_group")


@app.route('/edit_group', methods=['GET', 'POST'])
def edit_group():
    form = GroupForm()

    if request.method == 'GET':

        group_id = request.args.get('group_id')
        db = PostgresDb()
        group = db.sqlalchemy_session.query(Group).filter(Group.group_id == group_id).one()

        # fill form and send to student
        form.group_id.data = group.group_id
        form.group_name.data = group.group_name
        form.group_faculty.data = group.group_faculty

        return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")

    else:

        if not form.validate():
            return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")
        else:
            db = PostgresDb()
            # find student
            group = db.sqlalchemy_session.query(Group).filter(Group.group_id == form.group_id.data).one()

            # update fields from form data
            group.group_id = form.group_id.data
            group.group_faculty = form.group_faculty.data
            group.group_name = form.group_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_group'))


@app.route('/delete_group')
def delete_group():
    group_id = request.args.get('group_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Group).filter(Group.group_id == group_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_group'))


# END STUDENT ORIENTED QUERIES ----------------------------------------------------------------------------------------

# DISCIPLINE ORIENTED QUERIES ---------------------------------------------------------------------------------------

@app.route('/subject', methods=['GET'])
def index_subject():
    db = PostgresDb()

    subject = db.sqlalchemy_session.query(Subject).all()

    return render_template('subject.html', subjects=subject)


@app.route('/new_subject', methods=['GET', 'POST'])
def new_subject():
    form = SubjectForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('subject_form.html', form=form, form_name="New subject",
                                   action="new_subject")
        else:
            subject_obj = Subject(
                subj_name=form.subject_name.data,
                subj_hours=form.subject_hours.data)
            db = PostgresDb()

            s = db.sqlalchemy_session.query(Subject).filter(Subject.subj_name == subject_obj.subj_name).all()
            if s:
                form.subject_name.errors = ["Subject already exists"]
                return render_template('subject_form.html', form=form, form_name="New subject", action="new_subject")

            db.sqlalchemy_session.add(subject_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_subject'))

    return render_template('subject_form.html', form=form, form_name="New subject", action="new_subject")


@app.route('/edit_subject', methods=['GET', 'POST'])
def edit_subject():
    form = SubjectForm()

    if request.method == 'GET':

        subject_name = request.args.get('subj_name')
        db = PostgresDb()

        # -------------------------------------------------------------------- filter for "and" google
        subject = db.sqlalchemy_session.query(Subject).filter(
            Subject.subj_name == subject_name).one()

        # fill form and send to discipline
        form.subject_name.data = subject.subj_name
        form.subject_hours.data = subject.subj_hours

        return render_template('subject_form.html', form=form, form_name="Edit subject", action="edit_subject")

    else:

        if not form.validate():
            return render_template('subject_form.html', form=form, form_name="Edit subject",
                                   action="edit_subject")
        else:
            db = PostgresDb()
            # find discipline
            subject = db.sqlalchemy_session.query(Subject).filter(
                Subject.subj_name == form.subject_name.data).one()

            # update fields from form data
            subject.subj_name = form.subject_name.data
            subject.subj_hours = form.subject_hours.data

            # s = db.sqlalchemy_session.query(Subject).filter(Subject.subj_name == subject.subj_name).all()
            # if s:
            #     form.subject_name.errors = ["Subject already exists"]
            #     return render_template('subject_form.html', form=form, form_name="New subject", action="new_subject")

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_subject'))


@app.route('/delete_subject')
def delete_subject():
    subject_name = request.args.get('subj_name')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Subject).filter(
        Subject.subj_name == subject_name).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_subject'))

# @app.route('/view_scedule', methods=['GET', 'POST'])
# def view_scedule():
#     form = ViewForm()
#     if request.method == 'POST':
#         if not form.validate():
#             return render_template('view_form.html', form=form, form_name="View scedule",
#                                    action="view_scedule")
#         else:
#             # db = PostgresDb()
#             scedule_obj1 = Scedule(group_id_fk=form.group_id_fk.data)
#         db = PostgresDb()
#
#         scedule1 = db.sqlalchemy_session.query(Scedule).filter(Scedule.group_id_fk == scedule_obj1.group_id_fk)
#
#         return render_template('view_scedule.html', scedules=scedule1)
#         db.sqlalchemy_session.add(scedule_obj)
#         db.sqlalchemy_session.commit()
#
#     return redirect(url_for('index_scedule'))


@app.route('/view', methods=['GET'])
def view_scedule():
    db = PostgresDb()

    scedule = db.sqlalchemy_session.query(Scedule).all()

    return render_template('view_form.html', scedules=scedule)


@app.route('/scedule', methods=['GET'])
def index_scedule():
    db = PostgresDb()

    scedule = db.sqlalchemy_session.query(Scedule).all()

    return render_template('scedule.html', scedules=scedule)


@app.route('/new_scedule', methods=['GET', 'POST'])
def new_scedule():
    form = SceduleForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('scedule_form.html', form=form, form_name="New scedule",
                                   action="new_scedule")
        else:
            scedule_obj = Scedule(
                group_id_fk=form.group_id_fk.data,
                teach_id_fk=form.teach_id_fk.data,
                subj_name_fk=form.subj_name_fk.data,
                auditorium=form.auditorium.data,
                times=form.times.data,
                days=form.days.data)
            db = PostgresDb()
            check = db.sqlalchemy_session.query(Scedule).filter(Scedule.group_id_fk == scedule_obj.group_id_fk,
                                                                Scedule.times == scedule_obj.times,
                                                                Scedule.days == scedule_obj.days).all()
            if check:
                form.group_id_fk.errors = ["Entity already exists"]
                return render_template('scedule_form.html', form=form, action="new_scedule")
            d = db.sqlalchemy_session.query(Group).filter(Group.group_id == scedule_obj.group_id_fk).all()
            if not d:
                form.group_id_fk.errors = ["No such group"]
                return render_template('scedule_form.html', form=form, form_name="New scedule", action="new_scedule")
            dd = db.sqlalchemy_session.query(Teacher).filter(Teacher.teacher_id == scedule_obj.teach_id_fk).all()
            if not dd:
                form.group_id_fk.errors = ["No such teacher"]
                return render_template('scedule_form.html', form=form, form_name="New scedule", action="new_scedule")
            ddd = db.sqlalchemy_session.query(Subject).filter(Subject.subj_name == scedule_obj.subj_name_fk).all()
            if not ddd:
                form.group_id_fk.errors = ["No such subject"]
                return render_template('scedule_form.html', form=form, form_name="New scedule", action="new_scedule")
            db.sqlalchemy_session.add(scedule_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_scedule'))

    return render_template('scedule_form.html', form=form, form_name="New scedule", action="new_scedule")


@app.route('/edit_scedule', methods=['GET', 'POST'])
def edit_scedule():
    form = SceduleForm()

    if request.method == 'GET':
        times, days, group_id_fk = request.args.get('times'), request.args.get('days'), request.args.get('group_id_fk')
        db = PostgresDb()

        # -------------------------------------------------------------------- filter for "and" google
        scedule = db.sqlalchemy_session.query(Scedule).filter(
            Scedule.times == times,
            Scedule.days == days,
            Scedule.group_id_fk == group_id_fk).one()

        # fill form and send to scedule
        form.group_id_fk.data = scedule.group_id_fk
        form.teach_id_fk.data = scedule.teach_id_fk
        form.subj_name_fk.data = scedule.subj_name_fk
        form.auditorium.data = scedule.auditorium
        form.times.data = scedule.times
        form.days.data = scedule.days


        return render_template('scedule_form.html', form=form, form_name="Edit scedule", action="edit_scedule")

    else:

        if not form.validate():
            return render_template('scedule_form.html', form=form, form_name="Edit scedule",
                                   action="edit_scedule")
        else:
            db = PostgresDb()
            # find discipline
            scedule = db.sqlalchemy_session.query(Scedule).filter(
                Scedule.times == form.times.data,
                Scedule.days == form.days.data,
                Scedule.group_id_fk == form.group_id_fk. data).one()

            # update fields from form data
            scedule.group_id_fk = form.group_id_fk.data
            scedule.teach_id_fk = form.teach_id_fk.data
            scedule.subj_name_fk = form.subj_name_fk.data
            scedule.auditorium = form.auditorium.data
            scedule.times = form.times.data
            scedule.day = form.days.data
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_scedule'))


@app.route('/delete_scedule')
def delete_scedule():
    times, days, group_id_fk = request.args.get('times'), request.args.get('days'), request.args.get('group_id_fk')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Scedule).filter(
        Scedule.times == times,
        Scedule.days == days,
        Scedule.group_id_fk == group_id_fk).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_scedule'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = ApplyForm()
    if request.method == 'GET':
        return render_template('login_form.html', form=form, form_name="login", action="login")

    if request.method == 'POST':
        if not form.validate():
            return render_template('login_form.html', form=form, form_name="login", action="login")

        # print(form.user_login.data)
        # print(form.user_pass.data)
        db = PostgresDb()
        apply = db.sqlalchemy_session.query(Apply).filter(Apply.user_email == form.user_login.data, Apply.user_pass == form.user_pass.data).all()
        if apply:
            if form.user_login.data == 'Admin@gmail.com' and form.user_pass.data == 'admin1111':
                log.Login(form.user_login.data, form.user_pass.data, isAdmin=True)
                return redirect(url_for('dashboard'))
            else:
                log.Login(form.user_login.data, form.user_pass.data)
                return redirect(url_for('view_scedule'))
        else:
            return render_template('login_form.html', form=form, form_name="login", action="login")


def findClass(input, data, classes):
    y = []
    for d in data:
        sum = 0.0
        for i in range(len(input)):
            sum += (input[i] - d[i]) ** 2
        y.append(math.exp(-sum) / 0.09)
    return classes[y.index(max(y))]

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    a = db.sqlalchemy_session.query(Scedule).all()
    teacher = [[2], [6], [10]]
    classes = ['Mostly-free', 'Middle-packed', 'Packed']
    table = {}
    audits = {}
    for s in a:
        audits[s.auditorium] = 0
    for s in a:
        audits[s.auditorium] +=1
    for audit in audits:
        table[audit] = findClass([audits[audit]],teacher,classes)

    return render_template('analysis.html', table = table)

@app.route('/new_apply', methods=['GET', 'POST'])
def new_apply():
    form = ApplyForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('apply_form.html', form=form, form_name="New Apply", action="new_apply")
        else:

            apply_obj = Apply(
                user_email=form.user_login.data,
                user_pass=form.user_pass.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(apply_obj)
            db.sqlalchemy_session.commit()
            return redirect(url_for('new_scedule'))

    return render_template('apply_form.html', form=form, form_name="New Apply", action="new_apply")


if __name__ == '__main__':
    db = PostgresDb()
    app.run(debug=True)
