import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import plotly
import plotly.graph_objs as go
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import *
from models import *
from NN import NN

DATABASE_URI = 'postgres://hlrldwefmepodr:eadd84caf40fd0621df5ce4ec0cae8d990aadd14bfefb5b1c902a611983430e2@ec2-54-195-252-243.eu-west-1.compute.amazonaws.com:5432/dbk946o84kbp1r'
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ksjdfhdsjkflhdsjklvn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
db = SQLAlchemy(app)

@app.route('/', methods=["GET", "POST"])
def home():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate():
            render_template('home.html', form=form)
        else:
            name = form.name.data
            password = form.password.data
            user = db.session.query(Users).filter(Users.user_name == name).filter(Users.pasword == password).all()
            #print('user' + str(user))
            if user:
                #print('full')
                if name == 'Admin':
                    return redirect(url_for('admin'))
                return redirect(url_for('cabinet', user=name))
            return render_template('home.html', form=form, message='not found')

    return render_template('home.html', form=form)

@app.route('/registration', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if not form.validate():
            render_template('registration.html', form=form)
        else:
            name = form.name.data
            age = form.age.data
            weight = form.weight.data
            height = form.hight.data
            password = form.password.data
            user_data = Users(
                user_name = name,
                age = age,
                pasword = password)
            activate_data = Activate(
                user_name = name,
                complex_name = 'start',
                time_start = datetime.now(),
                status = 'NULL',
                weight = weight,
                hight = height)
            try:
                db.session.add(user_data)
                db.session.commit()
                db.session.add(activate_data)
                db.session.commit()
                return redirect(url_for('cabinet', user=name))
            except:
                return render_template('registration.html', form=form, message='User already exist')

    return render_template('registration.html', form=form)

@app.route('/users', methods=["GET", "POST"])
def users():
    complex_all = db.session.query(Users).all()
    return render_template('users.html', complexAll=complex_all)

@app.route('/admin', methods=["GET", "POST"])
def admin():
    return render_template('admin.html')

@app.route('/cabinet', methods=["GET", "POST"])
def cabinet():
    name = request.args.get('user')

    return render_template('cabinet.html', user=name)

@app.route('/plan', methods=["GET", "POST"])
def plan():
    name = request.args.get('user')

    return render_template('plan.html', user=name)

@app.route('/massenger', methods=["GET", "POST"])
def massenger():
    name = request.args.get('user')

    return render_template('massenger.html', user=name)

@app.route('/complex', methods=["GET"])
def complex():
    complex_all = db.session.query(Complex).all()
    return render_template('complex.html', complexAll=complex_all)

@app.route('/complex_create', methods=["GET", "POST"])
def complex_create():
    form = ComplexForm()
    if request.method == 'POST':
        if not form.validate():
            render_template('complex_create.html', form=form, form_name='Create complex')
        else:
            try:
                complex_data = Complex(
                    complex_name = form.name.data,
                    complex_level = form.level.data
                )
                db.session.add(complex_data)
                db.session.commit()
                return redirect(url_for('complex'))
            except:
                message = 'You cant delete this'
                return render_template('error.html', message=message)

    return render_template('complex_create.html', form=form, form_name='Create complex')

@app.route('/complex_update', methods=['GET','POST'])
def complex_update():
    form = ComplexForm()
    name = request.args.get('name')
    if request.method == 'GET':

        field = db.session.query(Complex).filter(Complex.complex_name == name).one()

        form.name.data = field.complex_name
        form.level.data = field.complex_level

        return render_template('complex_create.html', form=form, form_name='Update complex')
    else:
        if not form.validate():
            return render_template('complex_create.html', form=form, form_name='Update complex')
        try:
            complexs = db.session.query(Complex).filter(Complex.complex_name == name).one()
            complexs.complex_name = form.name.data
            complexs.complex_level = form.level.data

            db.session.commit()
            return redirect(url_for('complex'))
        except:
            message = 'You cant delete this'
            return render_template('error.html', message=message)

@app.route('/delete_complex')
def delete_complex():
    name = request.args.get('name')
    try:
        db.session.delete(db.session.query(Complex).filter(Complex.complex_name == name).one())
        db.session.commit()
        return redirect(url_for('complex'))
    except:
        message = 'You cant delete this'
        return render_template('error.html', message=message)


@app.route('/exercise', methods=["GET"])
def exercise():
    exercise_all = db.session.query(Exercise).all()
    return render_template('exercise.html', complexAll=exercise_all)

@app.route('/exercise_create', methods=["GET", "POST"])
def exercise_create():
    form = ExerciseForm()
    if request.method == 'POST':
        if not form.validate():
            render_template('exercise_create.html', form=form, form_name='Create exercise')
        else:
            try:
                exercise_data = Exercise(
                    exercise_name = form.name.data,
                    information = form.info.data
                )
                db.session.add(exercise_data)
                db.session.commit()
                return redirect(url_for('exercise'))
            except:
                message = 'You cant delete this'
                return render_template('error.html', message=message)

    return render_template('exercise_create.html', form=form, form_name='Create exercise')

@app.route('/exercise_update', methods=['GET','POST'])
def exercise_update():
    form = ExerciseForm()
    name = request.args.get('name')
    if request.method == 'GET':

        field = db.session.query(Exercise).filter(Exercise.exercise_name == name).one()

        form.name.data = field.exercise_name
        form.info.data = field.information

        return render_template('exercise_create.html', form=form, form_name='Update exercise')
    else:
        if not form.validate():
            return render_template('exercise_create.html', form=form, form_name='Update exercise')
        try:
            complexs = db.session.query(Exercise).filter(Exercise.exercise_name == name).one()
            complexs.exercise_name = form.name.data
            complexs.information = form.info.data

            db.session.commit()
            return redirect(url_for('exercise'))
        except:
            message = 'You cant delete this'
            return render_template('error.html', message=message)

@app.route('/delete_exercise')
def delete_exercise():
    name = request.args.get('name')
    try:
        db.session.delete(db.session.query(Exercise).filter(Exercise.exercise_name == name).one())
        db.session.commit()
        return redirect(url_for('exercise'))
    except:
        message = 'You cant delete this'
        return render_template('error.html', message=message)


@app.route('/complex_exercise', methods=["GET"])
def complex_exercise():
    che_all = db.session.query(Complex_has_exercise).all()
    return render_template('complex_exercise.html', complexAll=che_all)

@app.route('/che_create', methods=["GET", "POST"])
def che_create():
    form = CheForm()
    if request.method == 'POST':
        if not form.validate():
            render_template('che_create.html', form=form, form_name='Create CHE')
        else:
            try:
                exercise_data = Complex_has_exercise(
                    complex_name = form.complex_name.data,
                    exercise_name = form.exercise_name.data,
                    repeater = form.repeater.data
                )
                db.session.add(exercise_data)
                db.session.commit()
                return redirect(url_for('complex_exercise'))
            except:
                message = 'You cant delete this'
                return render_template('error.html', message=message)

    return render_template('che_create.html', form=form, form_name='Create CHE')

@app.route('/che_update', methods=['GET','POST'])
def che_update():
    form = CheForm()
    complex_name = request.args.get('cn')
    exercise_name = request.args.get('en')
    if request.method == 'GET':

        field = db.session.query(Complex_has_exercise).filter(Complex_has_exercise.exercise_name == exercise_name).filter(Complex_has_exercise.complex_name == complex_name).one()

        form.complex_name.data = field.complex_name
        form.exercise_name.data = field.exercise_name
        form.repeater.data = field.repeater

        return render_template('che_create.html', form=form, form_name='Update CHE')
    else:
        if not form.validate():
            return render_template('che_create.html', form=form, form_name='Update CHE')
        try:
            complexs = db.session.query(Complex_has_exercise).filter(Complex_has_exercise.exercise_name == exercise_name).filter(Complex_has_exercise.complex_name == complex_name).one()
            complexs.exercise_name = form.exercise_name.data
            complexs.complex_name = form.complex_name.data
            complexs.repeater = form.repeater.data

            db.session.commit()
            return redirect(url_for('complex_exercise'))
        except:
            message = 'You cant delete this'
            return render_template('error.html', message=message)


@app.route('/delete_che')
def delete_che():
    complex_name = request.args.get('cn')
    exercise_name = request.args.get('en')
    try:
        db.session.delete(db.session.query(Complex_has_exercise).filter(Complex_has_exercise.exercise_name == exercise_name).filter(Complex_has_exercise.complex_name == complex_name).one())
        db.session.commit()
        return redirect(url_for('complex_exercise'))
    except:
        message = 'You cant delete this'
        return render_template('error.html', message=message)

from sqlalchemy import func, join
@app.route('/gene')
def gene():
    name = request.args.get('user')
    #max_date = db.session.query(Activate.time_start).filter(Activate.user_name == name).limit(1)
    #max_date = maxx_date.time_start
    max_date = db.session.query(func.max(Activate.time_start)).filter(Activate.user_name == name).scalar()
    print(max_date)
    #max_date = maxx_date.time_start.max()
    params = db.session.query(Activate).all()
    users = [obj.user_name for obj in params]
    age = []
    for u in users:
        a = db.session.query(Users).filter(Users.user_name == u).one().age
        age.append((date.today()-a).days // 365)
    complexes = [obj.complex_name for obj in params]
    level = []
    for l in complexes:
        l = db.session.query(Complex).filter(Complex.complex_name == l).one().complex_level
        level.append(l)
    weight = [obj.weight for obj in params]
    height = [obj.hight for obj in params]
    #final = []
    #for i in len(weight):
    #    final.append([age[i], weight[i], height[i], level[i]])
    start = [obj.time_start for obj in params]
    hour = [dat.hour for dat in start]
    status = [obj.status for obj in params]
    df = pd.DataFrame(columns=['hour', 'status'])
    df.hour = hour
    df.status = status
    productivity = []
    for i in range(24):
        done = df[(df.hour == i) & (df.status == 'done')].shape[0]
        all = df[df.hour == i].shape[0]
        if all != 0:
            productivity.append((done/all))
        else:
            productivity.append(0)
    res_hour = productivity.index(max(productivity))
    dictt = {'light': 1, 'middle': 2, 'hard': 3}
    level_int = []
    for i in level:
        level_int.append([value  for (key, value) in dictt.items() if key == i][0])
    df2 = pd.DataFrame(columns=['age', 'weight', 'height'])
    df2.age = age
    df2.weight = weight
    df2.height = height
    clf = RandomForestClassifier(random_state=0, max_depth=2)
    clf.fit(df2, level_int)
    print(df2.shape, len(level_int))
    field = db.session.query(Activate).filter(Activate.user_name == name).filter(Activate.time_start == max_date).one()


    age_pr = (date.today()-db.session.query(Users).filter(Users.user_name == name).one().age).days // 365
    res_level = clf.predict([[age_pr, field.weight, field.hight]])
    #sample = np.array([[age_pr, field.weight,field.hight]])
    #print(sample)
    #print(clf.predict([[age_pr, field.weight,field.hight]]))
    print(res_hour, res_level)
    cmpl_lvl = [key for (key, value) in dictt.items() if value == res_level[0]][0]
    cmpl_name = db.session.query(Complex).filter(Complex.complex_level == cmpl_lvl).order_by(func.random()).first().complex_name
    print(cmpl_name)
    #cmpl = db.session.query(Complex_has_exercise).filter(Complex_has_exercise.complex_name == cmpl_name).all()
    cmpl = db.session.query(Complex_has_exercise.exercise_name,Complex_has_exercise.repeater, Exercise.information).filter(Complex_has_exercise.exercise_name == Exercise.exercise_name).filter(Complex_has_exercise.complex_name == cmpl_name).all()
    #db.session.query(Exercise).filter

    return render_template('plan.html', user=name, cmpl=cmpl,weight=field.weight, height=field.hight, cmpl_name=cmpl_name, message="Best hour = "+str(res_hour)+"; Best complex = "+str(cmpl_name))
    #res = NN(params=, input_data=, level=)

@app.route('/update', methods=['GET','POST'])
def update():
    name = request.args.get('user')
    complex = request.args.get('complex')
    status = request.args.get('status')
    weight = request.args.get('weight')
    height = request.args.get('height')

    form = Update()
    if request.method == 'GET':

        form.weight.data = weight
        form.hight.data = height

        return render_template('update.html', user=name, cmpl=complex, weight=weight, height=height, status=status, form=form)
    if request.method == 'POST':
        if not form.validate():
            render_template('update.html', user=name, cmpl=complex, weight=weight, height=height, status=status, form=form)
        else:
            user_data = Activate(
                user_name=name,
                complex_name=complex,
                time_start=datetime.now(),
                status=status,
                weight=form.weight.data,
                hight=form.hight.data
            )
            db.session.add(user_data)
            db.session.commit()
            return render_template('cabinet.html', user=name)
    return render_template('update.html', user=name, cmpl=complex, weight=weight, height=height, status=status, form=form)



'''
@app.route('/dashboard')
def rejects():
    data = db.session.query(User_do_complex).all()
    datee = [obj.time_start for obj in data]
    status = [obj.status for obj in data]
    hour = [dat.hour for dat in datee]
    df = pd.DataFrame(columns=['hour','status'])
    df.hour = hour
    df.status = status
    df1 = df[df.status.isin(['done', 'rejected'])].groupby('hour').status.count().reset_index()
    df2 = df[df.status == 'rejected'].groupby('hour').status.count().reset_index()
    df_res = pd.merge(df1,df2,how='left',on='hour')
    df_res.columns = ['hour', 'alll', 'rej']
    df_res.rej.fillna(0,inplace=True)
    df_res['ratio'] = df_res.rej / df_res.alll

    bar = go.Bar(x=df_res.hour, y=df_res.ratio)

    #print(df_res.hour, df_res.ratio)
    graphJSON = json.dumps([bar], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', graphJSON=graphJSON,ids=[0])

@app.route('/scatter')
def scatter():
    data = db.session.query(Users).all()
    datee = [obj.age for obj in data]
    weight = [obj.weight for obj in data]
    activity = [obj.activity for obj in data]
    age = [(date.today() - dat).days // 365 for dat in datee]

    scatter = go.Scatter(x=age, y=activity,mode='markers',marker_size=weight)

    #print(age)
    graphJSON = json.dumps([scatter], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', graphJSON=graphJSON,ids=[0])
'''

if __name__ == '__main__':
    app.run(debug=True)
