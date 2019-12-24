from datetime import datetime, timedelta

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sqlalchemy import Integer, String, Date, func, Sequence, Table, Column, ForeignKey, text
from sqlalchemy.orm import relationship

from forms.clubform import editClub
from forms.event_form import EditEvent
from forms.plan_form import CreatePlan, EditPlan
from forms.searchform import CreateQuery
from forms.user_form import EditUser
from forms.formBonus import BonusForm
from forms.CreateBonusForm import CreateBonus
import plotly
import plotly.graph_objs as go
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from neupy import algorithms

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ohrydko:meizu123@localhost/postgres'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://kdvqrwpolqqdxf:25c2172ddfb69bd5e5990b291e259f9f4c67608d2c79f257cd4cfb7c7a510241@ec2-107-20-167-241.compute-1.amazonaws.com:5432/d397i23882m0pu'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

list_event = []


class ormUser(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(Integer, Sequence('users_id_seq', start=1, increment=1), primary_key=True)
    name = db.Column(String(40))
    surname = db.Column(String(40))
    birthday = db.Column(Date)
    userRelationShip = db.relationship("ormEvent", back_populates="user_Relation_Ship")


association_table = Table('association', db.metadata,
                          Column('left_id', String, ForeignKey('club.address')),
                          Column('right_id', Integer, ForeignKey('event.event_id')))


class ormEvent(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(Integer, Sequence('event_id_seq', start=1, increment=1), primary_key=True)
    name = db.Column(String(40))
    user_id_fk = db.Column(Integer, db.ForeignKey('user.user_id'))
    category = db.Column(String(40))
    city = db.Column(String(40))
    dates = db.Column(Date)
    price = db.Column(Integer)
    hashtag = db.Column(String(40))
    adress = db.Column(String(40))
    count_of_people = db.Column(Integer)
    user_Relation_Ship = db.relationship("ormUser", back_populates="userRelationShip")
    parent = relationship("ormClub", secondary=association_table)


class ormClub(db.Model):
    __tablename__ = 'club'
    address = db.Column(String(40), primary_key=True)
    name = db.Column(String(40))
    price = db.Column(Integer)
    year_open = db.Column(Integer)
    children = relationship("ormEvent", secondary=association_table)


class ormPlan(db.Model):
    __tablename__ = 'plan'
    event_id = db.Column(Integer, primary_key=True)
    newSkill = db.Column(String(40))
    description = db.Column(String(40))
    company = db.Column(String(40))
    category = db.Column(String(40))


class ormBonus(db.Model):
    __tablename__ = 'bonus'

    event_id = db.Column(Integer, primary_key=True)
    name = db.Column(String(40))
    value = db.Column(String(40))


@app.route('/get')
def addClub():
    event1 = ormEvent(event_id=28, name="Sasha", user_id_fk=3, category="cat",
                      city="kyiv", dates="2019-12-12", price=100, hashtag="a", adress="kyiv")
    club1 = ormClub(address="asd", name="sa", price=100, year_open=1927)

    event2 = ormEvent(event_id=29, name="Sasha", user_id_fk=3, category="cat",
                      city="kyiv", dates="2019-12-12", price=100, hashtag="a", adress="kyiv")
    club2 = ormClub(address="sdf", name="sa", price=1000, year_open=1927)

    event3 = ormEvent(event_id=30, name="Sasha", user_id_fk=3, category="cat",
                      city="kyiv", dates="2019-12-12", price=100, hashtag="a", adress="kyiv")
    club3 = ormClub(address="fg", name="sa", price=112, year_open=1927)

    event1.parent.append(club1)
    club1.children.append(event1)
    event2.parent.append(club2)
    club2.children.append(event2)
    event3.parent.append(club3)
    club3.children.append(event3)

    db.session.add_all([event1, club1, event2, event3, club2, club3])
    db.session.commit()
    return render_template('index.html', action="/")


@app.route('/')
def hello_world():
    return render_template('index.html', action="/")


@app.route('/dashboard')
def dashboard():
    query1 = (
        db.session.query(
            func.count(),
            ormPlan.category
        ).group_by(ormPlan.category)
    ).all()

    query = (
        db.session.query(
            func.count(ormEvent.hashtag),
            ormEvent.dates
        ).group_by(ormEvent.dates)
    ).all()

    dates, counts = zip(*query)
    bar = go.Bar(
        x=counts,
        y=dates
    )

    skills, user_count = zip(*query1)
    pie = go.Pie(
        labels=user_count,
        values=skills
    )
    print(dates, counts)
    print(skills, user_count)

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = CreateQuery()
    if request.method == 'POST':
        if not form.validate() or form.validate_on_submit() == False:
            if not form.validate_on_submit():
                form.date.errors = "date > 1900"
            return render_template('search.html', form=form, form_name="Search", action="search")
        else:
            list_event.clear()
            for id, category, city, dates in db.session.query(ormEvent.event_id, ormEvent.category, ormEvent.city,
                                                              ormEvent.dates):
                if category == form.name_of_event.data and city == form.city.data and dates == form.date.data:
                    list_event.append(id)

            return redirect(url_for('searchList'))

    return render_template('search.html', form=form, form_name="Search", action="search")


@app.route('/search/result')
def searchList():
    res = []
    try:
        for i in list_event:
            name, new_skill, hashtag, city, dates, bonus = db.session \
                .query(ormEvent.name, ormPlan.newSkill, ormEvent.hashtag, ormEvent.city, ormEvent.dates, ormBonus.name) \
                .join(ormBonus, ormEvent.event_id == ormBonus.event_id).join(ormPlan,
                                                                             ormEvent.event_id == ormPlan.event_id) \
                .filter(ormEvent.event_id == i).one()
            res.append(
                {"name": name, "new_skill": new_skill, "hashtag": hashtag, "city": city, "dates": dates,
                 "bonus": bonus})
    except:
        print("don't data")
    print(list_event)

    return render_template('search_list_event.html', name="result", results=res, action="/search/result")


@app.route('/show')
def all_club():
    name = "club"

    bonus_db = db.session.query(ormClub).all()
    bonus = []
    for row in bonus_db:
        bonus.append({"address": row.address, "name": row.name, "price": row.price, "year_open": row.year_open})
    return render_template('allClub.html', name=name, bonus=bonus, action="/show")


@app.route('/all/bonus')
def all_bonus():
    name = "bonus"
    name = "bonus"

    bonus_db = db.session.query(ormBonus).all()
    bonus = []
    for row in bonus_db:
        bonus.append({"event_id": row.event_id, "name": row.name, "value": row.value})
    return render_template('allBonus.html', name=name, bonus=bonus, action="/all/bonus")


@app.route('/all/event')
def all_event():
    name = "event"

    event_db = db.session.query(ormEvent).all()
    event = []
    for row in event_db:
        event.append(
            {"event_id": row.event_id, "name": row.name, "user_id_fk": row.user_id_fk, "category": row.category,
             "city": row.city, "dates": row.dates, "price": row.price, "hashtag": row.hashtag, "adress": row.adress,
             "count_of_people": row.count_of_people})
    return render_template('all_event.html', name=name, events=event, action="/all/event")


@app.route('/all/user')
def all_user():
    name = "user"

    bonus_db = db.session.query(ormUser).all()
    user = []
    for row in bonus_db:
        user.append({"user_id": row.user_id, "name": row.name, "surname": row.surname, "birthday": row.birthday})
    return render_template('allUser.html', name=name, users=user, action="/all/user")


@app.route('/all/plan')
def all_plan():
    name = "plan of event"

    plan_db = db.session.query(ormPlan).all()
    plan = []
    for row in plan_db:
        plan.append({"event_id": row.event_id, "newSkill": row.newSkill, "description": row.description,
                     "company": row.company, "category": row.category})
    return render_template('all_plan.html', name=name, plans=plan, action="/all/plan")


@app.route('/create/bonus', methods=['GET', 'POST'])
def create_bonus():
    form = CreateBonus()
    ids = db.session.query(ormEvent).all()
    check = False
    for row in ids:
        if row.event_id == form.event_id.data:
            check = True
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_bonus.html', form=form, form_name="New bonus", action="create/bonus")
        else:
            id = db.session.query(ormBonus).all()
            checka = True
            for row in id:
                if row.event_id == form.event_id.data:
                    checka = False

            if check:
                if checka:
                    new_var = ormBonus(
                        event_id=form.event_id.data,
                        name=form.name.data,
                        value=form.value.data,

                    )
                    db.session.add(new_var)
                    db.session.commit()
                    return redirect(url_for('all_bonus'))
                else:
                    form.event_id.errors = "this event already exist"
            else:
                form.event_id.errors = "no event"

    return render_template('create_bonus.html', form=form, form_name="New bonus", action="create/bonus")


@app.route('/create/event', methods=['GET', 'POST'])
def create_event():
    form = EditEvent()

    if request.method == 'POST':
        if form.validate() == False or form.validate_on_submit() == False:

            if form.validate_on_submit() == False:
                form.birthday.errors = 'enter correct date > 1900'
            return render_template('event.html', form=form, form_name="New event", action="create/event")
        else:
            ids = db.session.query(ormUser).all()
            check = False
            for row in ids:
                if row.user_id == form.user_id_fk.data:
                    check = True
            if check:
                new_var = ormEvent(
                    name=form.name.data,
                    user_id_fk=form.user_id_fk.data,
                    category=form.category.data,
                    city=form.city.data,
                    dates=form.dates.data,
                    price=form.price.data,
                    hashtag=form.hashtag.data,
                    adress=form.adress.data,
                    count_of_people=form.count_of_people.data
                )

                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_event'))
            else:
                form.user_id_fk.errors = "no user with this id"

    return render_template('event.html', form=form, form_name="New event", action="create/event")


@app.route('/create/plan', methods=['GET', 'POST'])
def create_plan():
    form = CreatePlan()
    ids = db.session.query(ormEvent).all()
    check = False
    for row in ids:
        if row.event_id == form.event_id.data:
            check = True
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_plan.html', form=form, form_name="New plan", action="create/plan")
        else:
            id = db.session.query(ormPlan).all()
            checka = True
            for row in id:
                if row.event_id == form.event_id.data:
                    checka = False

            if check:
                if checka:
                    new_var = ormPlan(
                        event_id=form.event_id.data,
                        newSkill=form.newSkill.data,
                        description=form.description.data,
                        company=form.company.data,
                        category=form.category.data

                    )
                    db.session.add(new_var)
                    db.session.commit()
                    return redirect(url_for('all_plan'))
                else:
                    form.event_id.errors = "this event alredy exists"
            else:
                form.event_id.errors = "no event"

    return render_template('create_plan.html', form=form, form_name="New plan", action="create/plan")


@app.route('/create/user', methods=['GET', 'POST'])
def create_user():
    form = EditUser()

    if request.method == 'POST':
        if form.validate() == False or form.validate_on_submit() == False:

            if form.validate_on_submit() == False:
                form.birthday.errors = 'enter correct date > 1900'
            return render_template('user.html', form=form, form_name="New user", action="create/user")
        else:

            new_var = ormUser(
                name=form.name.data,
                surname=form.surname.data,
                birthday=form.birthday.data
            )

            db.session.add(new_var)
            db.session.commit()
            return redirect(url_for('all_user'))

    return render_template('user.html', form=form, form_name="New user", action="create/user")


@app.route('/delete/plan', methods=['GET'])
def delete_plan():
    event_id = request.args.get('event_id')

    result = db.session.query(ormPlan).filter(ormPlan.event_id == event_id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_plan'))


@app.route('/delete/event', methods=['GET'])
def delete_event():
    event_id = request.args.get('event_id')

    result = db.session.query(ormEvent).filter(ormEvent.event_id == event_id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_event'))


@app.route('/delete/user', methods=['GET'])
def delete_user():
    user_id = request.args.get('user_id')

    result = db.session.query(ormUser).filter(ormUser.user_id == user_id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_user'))


@app.route('/delete/bonus', methods=['GET'])
def delete_bonus():
    event_id = request.args.get('event_id')

    result = db.session.query(ormBonus).filter(ormBonus.event_id == event_id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_bonus'))


@app.route('/plot')
def plot():
    stmt = text('''select left_id as namess,count(right_id) as countss from association group by left_id;''')

    query1 = (db.session.query("namess", "countss").from_statement(stmt)
              ).all()

    query = (
        db.session.query(
            func.count(ormEvent.hashtag),
            ormEvent.dates
        ).group_by(ormEvent.dates)
    ).all()

    dates, counts = zip(*query)
    bar = go.Bar(
        x=counts,
        y=dates
    )

    skills, user_count = zip(*query1)
    pie = go.Pie(
        labels=skills,
        values=user_count
    )

    print(dates, counts)
    print(skills, user_count)

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/edit/club', methods=['GET', 'POST'])
def edit_club():
    form = editClub()
    address = request.args.get('address')
    if request.method == 'GET':

        bonus = db.session.query(ormClub).filter(ormClub.address == address).one()

        # fill form and send to user

        form.adress.data = bonus.address
        form.name.data = bonus.name
        form.price.data = bonus.price
        form.year.data = bonus.year_open

        return render_template('editClub.html', form=form, form_name="Edit user",
                               action="edit/club?address=" + address)


    else:

        if form.validate() == False or form.validate_on_submit() == False:
            return render_template('editClub.html', form=form, form_name="Edit user",
                                   action="edit/club?address=" + address)
        else:

            # find user
            var = db.session.query(ormClub).filter(ormClub.address == address).one()
            print(var)

            # update fields from form data

            var.address = form.adress.data
            var.name = form.name.data
            var.price = form.price.data
            var.year_open = form.year.data
            db.session.commit()

            return redirect(url_for('all_club'))


@app.route('/edit/user', methods=['GET', 'POST'])
def edit_user():
    form = EditUser()
    user_id = request.args.get('user_id')
    if request.method == 'GET':

        bonus = db.session.query(ormUser).filter(ormUser.user_id == user_id).one()

        # fill form and send to user

        form.name.data = bonus.name
        form.surname.data = bonus.surname
        form.birthday.data = bonus.birthday

        return render_template('user.html', form=form, form_name="Edit user",
                               action="edit/user?user_id=" + user_id)


    else:
        print(form.validate_on_submit())
        if form.validate() == False or form.validate_on_submit() == False:

            if form.validate_on_submit() == False:
                form.birthday.errors = 'enter correct date > 1900'
            return render_template('user.html', form=form, form_name="Edit user",
                                   action="edit/user?user_id=" + user_id)
        else:

            # find user
            var = db.session.query(ormUser).filter(ormUser.user_id == user_id).one()
            print(var)

            # update fields from form data

            var.name = form.name.data
            var.surname = form.surname.data
            var.birthday = form.birthday.data
            db.session.commit()

            return redirect(url_for('all_user'))


@app.route('/edit/bonus', methods=['GET', 'POST'])
def edit_bonus():
    form = BonusForm()
    event_id = request.args.get('event_id')
    if request.method == 'GET':

        bonus = db.session.query(ormBonus).filter(ormBonus.event_id == event_id).one()

        # fill form and send to user

        form.name.data = bonus.name
        form.value.data = bonus.value

        return render_template('bonus.html', form=form, form_name="Edit bonus",
                               action="edit/bonus?event_id=" + event_id)
    else:

        if form.validate() == False:
            return render_template('bonus.html', form=form, form_name="Edit bonus", action="edit/bonus")
        else:

            # find user
            var = db.session.query(ormBonus).filter(ormBonus.event_id == event_id).one()
            print(var)

            # update fields from form data

            var.name = form.name.data
            var.value = form.value.data

            db.session.commit()

            return redirect(url_for('all_bonus'))


@app.route('/edit/event', methods=['GET', 'POST'])
def edit_event():
    form = EditEvent()
    event_id = request.args.get('event_id')
    ids = db.session.query(ormUser)
    check = False
    for row in ids:
        if row.user_id == form.user_id_fk.data:
            check = True

    print(check)
    if request.method == 'GET':

        bonus = db.session.query(ormEvent).filter(ormEvent.event_id == event_id).one()

        # fill form and send to user

        form.name.data = bonus.name
        form.user_id_fk.data = bonus.user_id_fk
        form.category.data = bonus.category
        form.city.data = bonus.city
        form.dates.data = bonus.dates
        form.price.data = bonus.price
        form.hashtag.data = bonus.hashtag
        form.adress.data = bonus.adress
        form.count_of_people.data = bonus.count_of_people
        return render_template('event.html', form=form, form_name="Edit event",
                               action="edit/event?event_id=" + event_id)
    else:

        if form.validate() == False or form.validate_on_submit() == False:
            if form.validate_on_submit() == False:
                form.dates.errors = "enter date > 1900"
            return render_template('event.html', form=form, form_name="Edit event",
                                   action="edit/event?event_id=" + event_id,
                                   )
        else:

            # find user
            var = db.session.query(ormEvent).filter(ormEvent.event_id == event_id).one()
            print(var)

            # update fields from form data

            var.name = form.name.data
            var.user_id_fk = form.user_id_fk.data

            var.category = form.category.data
            var.city = form.city.data
            var.dates = form.dates.data
            var.price = form.price.data
            var.hashtag = form.hashtag.data
            var.adress = form.adress.data
            var.count_of_people = form.count_of_people.data

            if check:
                db.session.commit()
                return redirect(url_for('all_event'))
            else:
                form.user_id_fk.errors = "no user"
                return render_template('event.html', form=form, form_name="Edit event",
                                       action="edit/event?event_id=" + event_id,
                                       )


@app.route('/edit/plan', methods=['GET', 'POST'])
def edit_plan():
    form = EditPlan()
    event_id = request.args.get('event_id')
    if request.method == 'GET':

        plan = db.session.query(ormPlan).filter(ormPlan.event_id == event_id).one()

        # fill form and send to user

        form.newSkill.data = plan.newSkill
        form.description.data = plan.description
        form.company.data = plan.company
        form.category.data = plan.category

        return render_template('edit_plan.html', form=form, form_name="Edit plan",
                               action="edit/plan?event_id=" + event_id)


    else:

        if form.validate() == False:
            return render_template('edit_plan.html', form=form, form_name="Edit plan", action="edit/plan")
        else:

            # find user
            var = db.session.query(ormPlan).filter(ormPlan.event_id == event_id).one()
            print(var)

            # update fields from form data

            var.newSkill = form.newSkill.data
            var.description = form.description.data
            var.company = form.company.data
            var.category = form.category.data

            db.session.commit()

            return redirect(url_for('all_plan'))


@app.route('/correlation', methods=['GET', 'POST'])
def correlation():
    filter_after = datetime.today() - timedelta(days=30)
    counts = []
    for hashtag, count, name in db.session.query(ormEvent.hashtag, func.count(ormEvent.dates),
                                                 func.max(ormEvent.name)).filter(ormEvent.dates <= datetime.today()) \
            .filter(ormEvent.dates >= filter_after).group_by(ormEvent.hashtag):
        counts.append({"hashtag": hashtag, "count_events": count, "name": name})

    seq = [x['count_events'] for x in counts]
    print(counts)
    res = ''
    for row in counts:
        if row['count_events'] == max(seq):
            res = row['name']
    return render_template('correlation.html', row=res)


@app.route('/correlations', methods=['GET', 'POST'])
def correlations():
    df = pd.DataFrame()

    for name, count, avg in db.session.query(ormEvent.name, func.count(ormEvent.name), func.avg(ormEvent.price)
                                             ).group_by(ormEvent.name):
        df = df.append({"count_event": float(count), "avg_price": float(avg)}, ignore_index=True)
    db.session.close()
    query = (
        db.session.query(ormEvent.name, func.count(ormEvent.name), func.avg(ormEvent.price)
                         ).group_by(ormEvent.name)
    ).all()

    scaler = StandardScaler()
    scaler.fit(df[["count_event"]])
    train_X = scaler.transform(df[["count_event"]])
    print(train_X, df[["avg_price"]])
    reg = LinearRegression().fit(train_X, df[["avg_price"]])

    test_array = [[5]]
    test = scaler.transform(test_array)
    result = reg.predict(test)

    name, price, user_count = zip(*query)
    scatter = go.Scatter(
        x=price,
        y=user_count,
        mode='markers',
        marker_color='rgba(255, 0, 0, 100)',
        name="data"
    )
    x_line = np.linspace(0, 10)
    y_line = x_line * reg.coef_[0, 0] + reg.intercept_[0]
    line = go.Scatter(
        x=x_line,
        y=y_line,
        mode='lines',
        marker_color='rgba(255, 149, 0, 1)',
        name="regression"
    )

    data = [scatter, line]

    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('regretion.html', graphsJSON=graphsJSON)


@app.route('/claster', methods=['GET', 'POST'])
def claster():
    df = pd.DataFrame()

    for company, category in db.session.query(ormPlan.company, ormPlan.category):
        df = df.append({"company": company, "category": category}, ignore_index=True)

    X = pd.get_dummies(data=df)
    print(X)
    count_clasters = len(df['category'].unique())
    print(count_clasters)
    kmeans = KMeans(n_clusters=count_clasters, random_state=0).fit(X)
    # print(kmeans)
    count_columns = len(X.columns)
    test_list = [0] * count_columns
    test_list[1] = 1
    test_list[-1] = 1
    print(test_list)
    # print(kmeans.labels_)
    print(kmeans.predict(np.array([test_list])))
    db.session.close()
    query1 = (
        db.session.query(
            func.count(),
            ormPlan.category
        ).group_by(ormPlan.category)
    ).all()

    skills, user_count = zip(*query1)
    pie = go.Pie(
        labels=user_count,
        values=skills
    )

    data = [pie]
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('claster.html', row=kmeans.predict(np.array([test_list]))[0],
                           count_claster=count_clasters, graphsJSON=graphsJSON)


@app.route('/clasification', methods=['GET', 'POST'])
def clasification():
    df = pd.DataFrame()
    for category, hashtag, count_of_people in db.session.query(ormEvent.category, ormEvent.hashtag, ormEvent.count_of_people):
        print(category, hashtag, count_of_people)
        df = df.append({"category": category, "hashtag": hashtag, "count_of_people": count_of_people}, ignore_index=True)
    # db.session.close()

    mean_p = df['count_of_people'].mean()
    df.loc[df['count_of_people'] < mean_p, 'quality'] = 0
    df.loc[df['count_of_people'] >= mean_p, 'quality'] = 1
    X = pd.get_dummies(data=df[['category', 'hashtag']])
    print(df)
    print(X)
    pnn = algorithms.PNN(std=10, verbose=False)
    pnn.train(X, df['quality'])

    count_columns = len(X.columns)
    test_list = [0] * count_columns
    test_list[1] = 1
    test_list[-1] = 1
    print(test_list)
    y_predicted = pnn.predict([test_list])
    result = "Ні"
    if y_predicted - 1 < 0.0000001:
        result = "Так"

    return render_template('clasification.html', y_predicted=result, test_data=test_list)

if __name__ == '__main__':
    app.run()
