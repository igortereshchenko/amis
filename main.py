import plotly
import plotly.graph_objs as go
import json

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from math import e

from flask import render_template, flash, request, redirect, session
from ORM import *
from WTForms import *

app.secret_key = 'development key'


@app.route('/corr/<subj1>&<subj2>', methods=['GET', 'POST'])
def corr(subj1, subj2):

    total_sheet1 = db.session.query(SubjectSheet.subj_name, SubjectSheet.study_book,
                                   db.func.sum(SubjectSheet.mark).label('total'))\
        .filter_by(subj_name=subj1)\
        .group_by(SubjectSheet.subj_name, SubjectSheet.study_book).all()

    total_sheet2 = db.session.query(SubjectSheet.subj_name, SubjectSheet.study_book,
                                   db.func.sum(SubjectSheet.mark).label('total'))\
        .filter_by(subj_name=subj2)\
        .group_by(SubjectSheet.subj_name, SubjectSheet.study_book).all()

    x = []
    for row in total_sheet1:
        x.append(row.total)
    y = []
    for row in total_sheet2:
        y.append(row.total)

    x = np.array(x)
    y = np.array(y)

    corr_coef = np.corrcoef(x, y)[1][0]
    y1 = min(y) - 10
    y2 = max(y) + 10
    x1 = corr_coef*y1
    x2 = corr_coef*y2

    scatter = go.Scatter(x=x, y=y, marker=dict(color='rgb(122, 122, 122)'), mode='markers',
                         name='Marks from ' + subj1 + ' and ' + subj2)
    line = go.Scatter(x=[x1, x2], y=[y1, y2], marker=dict(color='rgb(50, 200, 200)'), mode='lines', name='Correlation')

    data = [scatter, line]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('correlatio.html',
                           graphJSON=graphJSON)


@app.route('/AI/<study_book>', methods=['GET', 'POST'])
def predict(study_book):

    def y1(W, X, i, sigma=0.3):

        res = sum(list(map(lambda j: e ** (-(W[j][i] - X[j]) ** 2 / sigma ** 2), range(len(W)))))

        return res

    def recognize(W1, X):

        Y1 = list(map(lambda i: y1(W1, X, i), range(len(W1[0]))))
        y_bad = sum(Y1[:6]) / 6
        y_ok = sum(Y1[6:9]) / 3
        y_good = sum(Y1[9:13]) / 4

        if y_good == max(y_bad, y_ok, y_good):
            return "It's good one!"
        elif y_ok == max(y_bad, y_ok, y_good):
            return "It's okay student!"
        else:
            return "It's bad student!"

    total_sheet = db.session.query(SubjectSheet.study_book, SubjectSheet.subj_name,
                                   db.func.sum(SubjectSheet.mark).label('total'))\
        .filter_by(study_book=study_book)\
        .group_by(SubjectSheet.study_book, SubjectSheet.subj_name).all()

    X = []
    for row in total_sheet:
        X.append(float(row.total))
    X += [0, 0, 0]
    X = X[:3]

    PNN_data = [[21, 98, 11, 'bad'], [26, 40, 55, 'bad'], [29, 44, 52, 'bad'], [40, 90, 2, 'bad'],
                [55, 42, 11, 'bad'], [33, 42, 56, 'bad'],
                [23, 60, 98, 'ok'], [60, 60, 60, 'ok'], [70, 70, 70, 'ok'],
                [75, 90, 70, 'good'], [80, 90, 100, 'good'], [78, 98, 70, 'good'], [100, 75, 70, 'good']]
    Weights = np.transpose(np.array(PNN_data))
    Weights = np.delete(Weights, 3, 0)
    Weights = np.asfarray(Weights, float)

    return recognize(Weights, X)


@app.route('/rating/<group_code>&<subj_name>', methods=['GET', 'POST'])
def rating(group_code=None, subj_name=None):

    total_sheet = db.session.query(SubjectSheet.group_code, SubjectSheet.subj_name, SubjectSheet.study_book,
                                   db.func.sum(SubjectSheet.mark).label('total'))\
        .filter_by(group_code=group_code, subj_name=subj_name)\
        .group_by(SubjectSheet.group_code, SubjectSheet.subj_name, SubjectSheet.study_book).all()
    if total_sheet == []:
        total_sheet = [{'group_code': group_code, 'subj_name': subj_name,
                        'study_book': 'No marks for this group', 'total': 'No marks = no total result'}]
    return render_template('rating.html', data=total_sheet)


@app.route('/cluster/<subj>', methods=['GET', 'POST'])
def cluster(subj):

    select_result = db.session.query(SubjectSheet.study_book, db.func.sum(SubjectSheet.mark).label('total'))\
        .filter_by(subj_name=subj).group_by(SubjectSheet.study_book).all()

    students_names = []
    total_marks = []
    for row in select_result:

        students_names.append(row.study_book)
        total_marks.append(row.total)

    df = pd.DataFrame(
        data=total_marks,
        index=students_names
    )

    kmeans = KMeans(n_clusters=3)
    kmeans.fit(df)

    labels = kmeans.predict(df)
    centroids = kmeans.cluster_centers_

    x = []
    for index, name in enumerate(students_names):
        x.append(index + 1)

    sct1 = go.Scatter(
        x = x,
        y = df[0],
        mode = 'markers',
        marker = dict(size = [10 for i in range(len(x))], color = [i + 2 for i in range(len(x))]),
        name = 'marks of students'
    )

    print(x)
    scts = [go.Scatter(
        x = [0, max(x) + 1],
        y = [centroid, centroid],
        mode = 'lines',
        marker = dict(color = [10, 10]),
        name = 'class ' + str(index + 1) + ' center'
    ) for index, centroid in enumerate(centroids.flatten())]

    data = [sct1] + scts

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("cluster.html", graphJSON=graphJSON)


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/edit_group', methods = ['GET', 'POST'])
def edit_group():

    form = GroupsForm()
    select_result = Groups.query.filter_by().all()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required')
            return render_template('groups.html', data=select_result, form=form)
        else:
            group_code = session['group_edit_pk_data']
            group = Groups.query.filter_by(code=group_code).first()
            group.code = form.code.data
            db.session.commit()
            return render_template("groups.html", data=select_result, form=form)

    return render_template("groups.html", data=select_result, form=form)


@app.route('/groups', methods=['GET', 'POST'])
def groups():

    form = GroupsForm()
    select_result = Groups.query.filter_by().all()

    if request.method == 'POST':

        selected_code = request.form.get('del')
        if selected_code is not None:
            selected_row = Groups.query.filter_by(code=selected_code).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            return render_template('groups.html', data=select_result, form=form)

        selected_code = request.form.get('edit')
        if selected_code is not None:
            selected_row = Groups.query.filter_by(code=selected_code).first()
            session['group_edit_pk_data'] = selected_code
            return render_template("edit_group.html", row=selected_row, form=form)

        print(form.validate())
        if not form.validate():
            flash('All fields are required.')
            return render_template('groups.html', data=select_result, form=form)
        else:
            group = Groups(form.code.data)
            db.session.add(group)
            db.session.commit()
            select_result.append(group)

    return render_template('groups.html', data=select_result, form=form)


@app.route('/edit_subject', methods=['GET', 'POST'])
def edit_subject():

    form = SubjectsForm()
    select_result = Subjects.query.filter_by().all()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('edit_subject.html')
        else:
            subject_name = session['subject_edit_pk_data']
            subject = Subjects.query.filter_by(name=subject_name).first()
            subject.name = form.name.data
            db.session.commit()
            return render_template("subjects.html", data=select_result, form=form)

    return render_template("subjects.html", data=select_result, form=form)


@app.route('/subjects', methods=['GET', 'POST'])
def subjects():

    form = SubjectsForm()
    select_result = Subjects.query.filter_by().all()

    if request.method == 'POST':

        selected_name = request.form.get('del')
        if selected_name is not None:
            selected_row = Subjects.query.filter_by(name=selected_name).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            return render_template('subjects.html', data=select_result, form=form)

        selected_name = request.form.get('edit')
        if selected_name is not None:
            selected_row = Subjects.query.filter_by(name=selected_name).first()
            session['subject_edit_pk_data'] = selected_name
            return render_template("edit_subject.html", row=selected_row, form=form)

        print(form.validate())
        if not form.validate():
            flash('All fields are required.')
            return render_template('subjects.html', data=select_result, form=form)
        else:
            subject = Subjects(form.name.data)
            db.session.add(subject)
            db.session.commit()
            select_result.append(subject)

    return render_template('subjects.html', data=select_result, form=form)


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():

    form = StudentsForm()
    select_result = Students.query.filter_by().all()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required')
            return render_template('students.html', data=select_result, form=form)
        else:
            selected_pk_data_list = session['student_edit_pk_data'].split("█")
            selected_group_code = selected_pk_data_list[0]
            selected_spooky_book = selected_pk_data_list[1]
            print(selected_group_code, selected_spooky_book)
            student = Students.query.filter_by(study_book=selected_spooky_book, group_code=selected_group_code).first()
            student.first_name = form.first_name.data
            student.last_name = form.last_name.data
            student.study_book = form.study_book.data
            student.group_code = form.group_code.data
            db.session.commit()
            return render_template("students.html", data=select_result, form=form)

    return render_template("students.html", data=select_result, form=form)


@app.route('/students', methods=['GET', 'POST'])
def students():

    form = StudentsForm()
    select_result = Students.query.filter_by().all()

    if request.method == 'POST':

        selected_pk_data = request.form.get('del')
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data.split("█")
            selected_group_code = selected_pk_data[0]
            selected_spooky_book = selected_pk_data[1]
            print(selected_spooky_book, selected_group_code)
            selected_row = Students.query.filter_by(study_book=selected_spooky_book, group_code=selected_group_code).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            return render_template('students.html', data=select_result, form=form)

        selected_pk_data = request.form.get('edit')
        if selected_pk_data is not None:
            selected_pk_data_list = selected_pk_data.split("█")
            selected_group_code = selected_pk_data_list[0]
            selected_spooky_book = selected_pk_data_list[1]
            selected_row = Students.query.filter_by(study_book=selected_spooky_book, group_code=selected_group_code).first()
            session['student_edit_pk_data'] = selected_pk_data
            return render_template("edit_student.html", row=selected_row, form=form)

        print(form.validate())
        if not form.validate():
            flash('All fields are required.')
            return render_template('students.html', data=select_result, form=form)
        else:
            student = Students(form.first_name.data, form.last_name.data, form.study_book.data, form.group_code.data)
            db.session.add(student)
            db.session.commit()
            select_result.append(student)

    return render_template('students.html', data=select_result, form=form)


@app.route('/edit_subjectsheet', methods=['GET', 'POST'])
def edit_subjectsheet():

    form = SubjectSheetForm()
    select_result = SubjectSheet.query.filter_by().all()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required')
            return render_template('subjectsheet.html', data=select_result, form=form)
        else:
            selected_pk_data_list = session['subjectsheet_edit_pk_data'].split("█")
            selected_subj_name = selected_pk_data_list[0]
            selected_group_code = selected_pk_data_list[1]
            selected_spooky_book = selected_pk_data_list[2]
            selected_date_of_mark = selected_pk_data_list[3]
            subjectsheet = SubjectSheet.query.filter_by(subj_name=selected_subj_name,
                                                        study_book=selected_spooky_book,
                                                        group_code=selected_group_code,
                                                        date_of_mark=selected_date_of_mark).first()
            subjectsheet.subj_name = form.subj_name.data
            subjectsheet.group_code = form.group_code.data
            subjectsheet.study_book = form.study_book.data
            subjectsheet.date_of_mark = form.date_of_mark.data
            subjectsheet.mark = form.mark.data
            db.session.commit()
            return render_template("subjectsheet.html", data=select_result, form=form)

    return render_template("subjectsheet.html", data=select_result, form=form)


@app.route('/subjectsheet', methods=['GET', 'POST'])
def subjectsheet():

    form = SubjectSheetForm()
    select_result = SubjectSheet.query.filter_by().all()

    if request.method == 'POST':

        selected_pk_data = request.form.get('del')
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data.split("█")
            selected_subj_name = selected_pk_data[0]
            selected_group_code = selected_pk_data[1]
            selected_spooky_book = selected_pk_data[2]
            selected_date_of_mark = selected_pk_data[3]
            selected_row = SubjectSheet.query.filter_by(subj_name=selected_subj_name, group_code=selected_group_code,
                                                    study_book=selected_spooky_book, date_of_mark=selected_date_of_mark).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            return render_template('subjectsheet.html', data=select_result, form=form)

        selected_pk_data = request.form.get('edit')
        if selected_pk_data is not None:
            selected_pk_data_list = selected_pk_data.split("█")
            selected_subj_name = selected_pk_data_list[0]
            selected_group_code = selected_pk_data_list[1]
            selected_spooky_book = selected_pk_data_list[2]
            selected_date_of_mark = selected_pk_data_list[3]
            selected_row = SubjectSheet.query.filter_by(subj_name=selected_subj_name,
                                                        study_book=selected_spooky_book,
                                                        group_code=selected_group_code,
                                                        date_of_mark=selected_date_of_mark).first()
            session['subjectsheet_edit_pk_data'] = selected_pk_data
            return render_template("edit_subjectsheet.html", row=selected_row, form=form)

        print(form.validate())
        if not form.validate():
            flash('All fields are required.')
            return render_template('subjectsheet.html', data=select_result, form=form)
        else:
            subjectsheet = SubjectSheet(form.subj_name.data, form.group_code.data, form.study_book.data,
                                        form.date_of_mark.data, form.mark.data)
            db.session.add(subjectsheet)
            db.session.commit()
            select_result.append(subjectsheet)

    return render_template('subjectsheet.html', data=select_result, form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    last_char = None
    if request.method == 'POST':

        last_char = request.form.get('last_char')
        if len(last_char) > 1:
            return redirect('/dashboard')

    select_result_raw = Groups.query.filter_by().all()
    if last_char is not None and last_char != "":
        select_result = [select_result_row.code for select_result_row in select_result_raw
                         if select_result_row.code[-1] == last_char]
    else:
        select_result = [select_result_row.code for select_result_row in select_result_raw]

    codes_starts_result = list(map(lambda s: s[:2], select_result))
    codes = list(set(codes_starts_result))
    counting_stars = [0] * len(codes)

    for no_more_counting_dollars in codes_starts_result:
        counting_stars[codes.index(no_more_counting_dollars[:2])] += 1

    bar, pie = go.Bar(x=codes, y=counting_stars, marker=dict(color='rgb(122, 122, 122)')), go.Pie(labels=codes, values=counting_stars)

    data1, data2 = [bar], [pie]
    ids = ["1", "2"]

    graphJSON1 = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html',
                           graphJSON1=graphJSON1, graphJSON2=graphJSON2, ids=ids)


if __name__ == '__main__':
    app.run(debug=True)