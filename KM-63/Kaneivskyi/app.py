from flask import Flask, render_template, request, redirect, url_for, session
from forms.CharacteristicForm import CharacteristicForm
from forms.EditCharacteristicForm import EditCharacteristicForm
from forms.EditGoodsForm import EditGoodsForm
from forms.EditStoreForm import EditStoreForm
from forms.GoodsForm import GoodsForm
from forms.StoreForm import StoreForm
from forms.UserForm import UserForm
from forms.EditUserForm import EditUserForm
from forms.SearchForm import CreateQuery
from forms.login_form import LoginForm
from forms.registration import RegistrationForm
import plotly
import json
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
from sqlalchemy.sql import func
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'qqq'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vlad16tank@localhost/postgres'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xmmsuctelhupxh:a9a963d03a98d1e263254d277d664accea5b167901a18dcf254e3c973d5ed453@ec2-107-22-160-185.compute-1.amazonaws.com:5432/dcm2lm1ecduiot'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    user_name = db.Column(db.String(20), primary_key=True)
    user_password = db.Column(db.String(15))
    u_good_id = db.relationship("Goods")


class Goods(db.Model):
    __tablename__ = 'goods'
    good_id = db.Column(db.Integer, primary_key=True)
    good_name = db.Column(db.String(45))
    good_model = db.Column(db.String(100))
    price=db.Column(db.Integer)

    stores = db.Column(db.Integer, db.ForeignKey('store.store_id'))
    users = db.Column(db.String(20), db.ForeignKey('user.user_name'))
    characters = db.relationship("Charac")


class Charac(db.Model):
    __tablename__ = 'charac'
    charac_name = db.Column(db.String(20), primary_key=True)
    charac_description = db.Column(db.String(100), primary_key=True)
    goods_fk = db.Column(db.Integer, db.ForeignKey('goods.good_id'))


class Store(db.Model):
    __tablename__ = 'store'
    store_id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(20), unique=True, nullable=False)
    store_link = db.Column(db.String(40), unique=True)
    good_id_store_fk = db.relationship("Goods")


# db.create_all()

# db.session.query(Charac).delete()
# db.session.query(Goods).delete()
# db.session.query(Store).delete()
# db.session.query(User).delete()

# Admin = User(
#     user_name="Admin",
#     user_password="ticheter"
# )
#
# User1 = User(
#     user_name="Vlad",
#     user_password="manager"
# )
#
# User2 = User(
#     user_name="Dima",
#     user_password="full-stack"
# )
# User3 = User(
#     user_name="Anya",
#     user_password="junior"
# )
# User4 = User(
#     user_name="Yar",
#     user_password="full-stack"
# )
# User5 = User(
#     user_name="Vano",
#     user_password="junior"
# )
#
# Good1 = Goods(
#     good_id=1,
#     good_name="Samsung",
#     good_model="S10",
#     price=1000,
#     stores=1,
#     users="Vlad")
#
# Good2 = Goods(
#     good_id=2,
#     good_name="OnePlus",
#     good_model="7 PRO",
#     price=2000,
#     stores=1,
#     users="Dima")
#
# Good3 = Goods(
#     good_id=3,
#     good_name="IPhone",
#     good_model="11",
#     price=3000,
#     stores=2,
#     users="Anya")
#
# Good4 = Goods(
#     good_id=4,
#     good_name="Huawei",
#     good_model="P30 PRO",
#     price=4000,
#     stores=2,
#     users="Yar")
#
# Good5 = Goods(
#     good_id=5,
#     good_name="Xiaomi Mi9",
#     good_model="Mi9",
#     stores=3,
#     price=5000,
#     users="Vano"
# )
#
# Charc1 = Charac(
#
#     charac_name="RAM",
#     charac_description="4Gb",
#     goods_fk=1
# )
# Charc2 = Charac(
#
#     charac_name="Color",
#     charac_description="black",
#     goods_fk=1)
#
# Charc3 = Charac(
#     charac_name="Capacity",
#     charac_description="64Gb",
#     goods_fk=1)
# Charc4 = Charac(
#
#     charac_name="Display",
#     charac_description="16:9",
#     goods_fk=1)
#
# Charc5 = Charac(
#
#     charac_name="Front Camera",
#     charac_description="12MP",
#     goods_fk=1)
# Charc6 = Charac(
#
#     charac_name="Count",
#     charac_description="11",
#     goods_fk=1)
#
# Charc7 = Charac(
#
#     charac_name="RAM",
#     charac_description="8Gb",
#     goods_fk=2
# )
# Charc8 = Charac(
#
#     charac_name="Color",
#     charac_description="yellow",
#     goods_fk=2)
# Charc9 = Charac(
#     charac_name="Capacity",
#     charac_description="128Gb",
#     goods_fk=2)
# Charc10 = Charac(
#
#     charac_name="Display",
#     charac_description="18:9",
#     goods_fk=2)
#
# Charc11 = Charac(
#
#     charac_name="Front Camera",
#     charac_description="18MP",
#     goods_fk=2)
#
# Charc12 = Charac(
#
#     charac_name="Count",
#     charac_description="10",
#     goods_fk=2)
#
# Store1 = Store(
#     store_id=1,
#     store_name="Rozetka",
#     store_link="https://rozetka.com.ua")
# Store2 = Store(
#     store_id=2,
#     store_name="Comfy",
#     store_link="https://comfy.com.ua")
# Store3 = Store(
#     store_id=3,
#     store_name="Citrus",
#     store_link="https://citrus.com.ua")
# Store4 = Store(
#     store_id=4,
#     store_name="Hotline",
#     store_link="https://hotline.com.ua")
# Store5 = Store(
#     store_id=5,
#     store_name="Allo",
#     store_link="https://allo.com.ua")
#
# # create relations
#
#
# Store1.good_id_store_fk.append(Good1)
# Store1.good_id_store_fk.append(Good2)
#
# Store1.good_id_store_fk.append(Good3)
# Store1.good_id_store_fk.append(Good4)
#
# Store1.good_id_store_fk.append(Good5)
#
#
#
# Good1.characters.append(Charc1)
# Good1.characters.append(Charc2)
# Good1.characters.append(Charc3)
# Good1.characters.append(Charc4)
# Good1.characters.append(Charc5)
# Good1.characters.append(Charc6)
#
# Good2.characters.append(Charc7)
# Good2.characters.append(Charc8)
# Good2.characters.append(Charc9)
# Good2.characters.append(Charc10)
# Good2.characters.append(Charc11)
# Good2.characters.append(Charc12)
#
# User1.u_good_id.append(Good1)
# User2.u_good_id.append(Good2)
# User3.u_good_id.append(Good3)
# User4.u_good_id.append(Good4)
# User5.u_good_id.append(Good5)
#
# # insert into database
# db.session.add_all([Charc1, Charc2, Charc3, Charc4, Charc5,Charc6, Charc7, Charc8, Charc9, Charc10,Charc11, Charc12])
# db.session.add_all([User1, User2, User3, User4, User5, Admin])
# db.session.add_all([Good1, Good2, Good3, Good4, Good5])
# db.session.add_all([Store1, Store2, Store3, Store4, Store5])
#
# db.session.commit()

list_goods = []
list_goods1 = []
res = []
name_c=[]
desc=[]

def dropSession():
    session['user_name'] = ''
    session['role'] = 'unlogged'

def newSession(name, pw):
    session['user_name'] = name
    if pw == 'ticheter':
        session['role'] = 'admin'
    else:
        session['role'] = 'user'

@app.route('/')
def root():
    if not session['user_name']:
        return redirect('/login')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate():
            try:
                res = db.session.query(User).filter(User.user_name == form.user_name.data).one()
            except:
                form.user_name.errors = ['user doesnt exist']
                return render_template('login.html', form=form)
            if res.user_password == form.user_password.data:
                newSession(res.user_name, res.user_password)
                return redirect('/')
            else:
                form.user_password.errors = ['wrong password']
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    else:

        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    dropSession()
    return redirect('/login')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate():
            new_user = User(
                user_email=form.user_email.data,
                user_password=form.user_confirm_password.data
            )
            db.session.add(new_user)
            db.session.commit()
            newSession(new_user.user_email, new_user.user_password)
            return render_template('success.html')
        else:
            return render_template('registration.html', form=form)

    return render_template('registration.html', form=form)


@app.route('/all_users')
def all_users():
    if session['role'] == 'admin':
        result = db.session.query(User).all()
        return render_template('all_users.html', result=result)
    else:
        return redirect('/login')

@app.route('/user/<string:name>')
def user_info(name):
    if session['role'] != 'unlogged':
        res = db.session.query(User).filter(User.user_name == name).one()
        return render_template('user_info.html', user=res)
    else:
        return redirect('/login')

@app.route('/all_users', methods=['GET'])
def user():
    if session['role'] == 'admin':
        result = db.session.query(User).all()
        return render_template('all_users.html', result=result)
    else:
        return redirect('/')



@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = UserForm()

    if request.method == 'POST':
        if form.validate():
            user = User(

                user_name=form.user_name.data,
                user_password=form.user_password.data,

            )
            try:
                db.session.add(user)
                db.session.commit()
                return redirect('/all_users')
            except:
                form.user_name.errors = ['this name already exists']

                return render_template('new_user_form.html', form=form, form_name="New user",
                                       action="new_user")
        else:
            if not form.validate():
                return render_template('new_user_form.html', form=form, form_name="New user",
                                   action="new_user")
    return render_template('new_user_form.html', form=form, form_name="New user",
                           action="new_user")

@app.route('/edit_user/<string:user_name>', methods=['GET', 'POST'])
def edit_user(user_name):
    form = EditUserForm()
    result = db.session.query(User).filter(User.user_name == user_name).one()

    if request.method == 'GET':

        form.user_name.data = result.user_name
        form.user_password.data = result.user_password

        return render_template('edit_user_form.html', form=form, form_name='edit user')
    elif request.method == 'POST':

        result.user_password = form.user_password.data
        db.session.commit()
    return redirect('/all_users')

@app.route('/all_characteristic', methods=['GET'])
def characteristic():
    if session['role'] == 'admin':
        result = db.session.query(Charac).all()
        return render_template('all_characteristic.html', result=result)
    else:
        return redirect('/')


@app.route('/new_characteristic', methods=['GET', 'POST'])
def new_characteristic():
    form = CharacteristicForm()

    if request.method == 'POST':
        if form.validate():
            new_characteristic = Charac(

                charac_name=form.charac_name.data,
                charac_description=form.charac_description.data,
                goods_fk=form.goods_fk.data

            )
            try:
                db.session.add(new_characteristic)
                db.session.commit()
                return redirect('/all_characteristic')
            except:
                form.goods_fk.errors = ['this id doen`t exists']

                return render_template('new_charactersitic_form.html', form=form, form_name="New characteristic",
                                       action="new_characteristic")
        else:
            if not form.validate():
                form.goods_fk.errors = ['should be between 0 and 100']

            return render_template('new_charactersitic_form.html', form=form, form_name="New characteristic",
                           action="new_characteristic")
    return render_template('new_charactersitic_form.html', form=form, form_name="New characteristic",
                           action="new_characteristic")


@app.route('/edit_characteristic/<string:charac_name>/<string:charac_description>', methods=['GET', 'POST'])
def edit_characteristic(charac_name,charac_description):
    form = EditCharacteristicForm()
    result = db.session.query(Charac).filter(Charac.charac_name == charac_name).filter(Charac.charac_description == charac_description).one()

    if request.method == 'GET':

        form.charac_name.data = result.charac_name
        form.charac_description.data = result.charac_description
        form.goods_fk.data = result.goods_fk


        charac_name = form.charac_name.data.replace("%20", " ")


        return render_template('edit_characteristic_form.html', form=form, form_name='edit characteristic')
    elif request.method == 'POST':
        if form.validate() and form.validate_on_submit():
            try:
                result.charac_name = charac_name
                result.charac_description = form.charac_description.data
                result.goods_fk = form.goods_fk.data

                db.session.commit()
                return redirect('/all_characteristic')
            except:
                form.goods_fk.errors = ['this id doesn`t exists']
                return render_template('edit_characteristic_form.html', form=form, form_name='edit characteristic')
        else:
            if not form.validate_on_submit():
                form.goods_fk.errors = ['should be > 0']
            return render_template('edit_characteristic_form.html', form=form, form_name='edit characteristic')


@app.route('/delete_characteristic/<string:charac_name>/<string:charac_description>', methods=['GET', 'POST'])
def delete_characteristic(charac_name, charac_description):
    result = db.session.query(Charac).filter(Charac.charac_name == charac_name).filter(
        Charac.charac_description == charac_description).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/all_characteristic')


@app.route('/all_goods', methods=['GET'])
def goods():
    if session['role'] == 'admin':
        result = db.session.query(Goods).all()
        return render_template('all_goods.html', result=result)
    else:
        return redirect('/')

@app.route('/new_goods', methods=['GET', 'POST'])
def new_goods():
    form = GoodsForm()

    if request.method == 'POST':
        if form.validate():
            new_goods = Goods(
                good_id=form.good_id.data,
                good_name=form.good_name.data,
                good_model=form.good_model.data,
                price= form.price.data,
                stores = form.stores.data,
                users = form.users.data,

            )
            try:
                db.session.add(new_goods)
                db.session.commit()
                return redirect(url_for('goods'))
            except:
                form.good_id.errors = ['This id already exists']
                form.stores.errors = ['This store doesn`t exists']
                form.users.errors = ['This user doesn`t exists']
                return render_template('new_goods_form.html', form=form, form_name="New goods", action="new_goods")
        else:
            if not form.validate():
                return render_template('new_goods_form.html', form=form, form_name="New goods", action="new_goods")
    elif request.method == 'GET':
        return render_template('new_goods_form.html', form=form, form_name="New goods", action="new_goods")


    return render_template('new_goods_form.html', form=form, form_name="New goods", action="new_goods")


@app.route('/edit_goods/<int:good_id>', methods=['GET', 'POST'])
def edit_goods(good_id):

    form = EditGoodsForm()
    result = db.session.query(Goods).filter(Goods.good_id == good_id).one()

    if request.method == 'GET':

        form.good_name.data = result.good_name
        form.good_model.data = result.good_model
        form.price.data = result.price
        form.stores.data = result.stores
        form.users.data = result.users

        return render_template('edit_goods_form.html', form=form, form_name='edit goods')
    elif request.method == 'POST':
        if form.validate() and form.validate_on_submit():
            try:
                result.good_name = form.good_name.data
                result.good_model = form.good_model.data
                result.price = form.price.data
                result.stores = form.stores.data
                result.users = form.users.data
                db.session.commit()
                return redirect('/all_goods')
            except:
                form.stores.errors=['This store doesn`t exists']
                form.users.errors = ['This user doesn`t exists']
                form.good_model.errors=['This model already exists']
                return render_template('edit_goods_form.html', form=form, form_name='edit goods')
        else:
            if not form.validate_on_submit():
                form.stores.errors = ['should be > 0']
    else:
                return render_template('edit_goods_form.html', form=form, form_name='edit goods')




@app.route('/delete_goods/<string:good_id>', methods=['GET', 'POST'])
def delete_goods(good_id):
    result = db.session.query(Goods).filter(Goods.good_id == good_id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/all_goods')


@app.route('/all_store', methods=['GET'])
def store():
    if session['role'] == 'admin':
        result = db.session.query(Store).all()
        return render_template('all_store.html', result=result)
    else:
        return redirect('/')


@app.route('/new_store', methods=['GET', 'POST'])
def new_store():
    form = StoreForm()

    if request.method == 'POST':
        if form.validate():
            try:

                new_store = Store(

                    store_id=form.store_id.data,
                    store_name=form.store_name.data,
                    store_link=form.store_link.data,


                )

                db.session.add(new_store)
                db.session.commit()

                return redirect(url_for('store'))
            except:
                form.store_id.errors = ['error uniq']
                return render_template('new_store_form.html', form=form, form_name="New store", action="new_store")

        else:
            form.store_id.errors = ['should be between 0 and 100']
            return render_template('new_store_form.html', form=form, form_name="New store", action="new_store")

    return render_template('new_store_form.html', form=form, form_name="New store", action="new_store")


@app.route('/edit_store/<string:store_name>', methods=['GET', 'POST'])
def edit_store(store_name):
    form = EditStoreForm()
    result = db.session.query(Store).filter(Store.store_name == store_name).one()

    if request.method == 'GET':

        form.store_name.data = result.store_name
        form.store_link.data = result.store_link

        return render_template('edit_store_form.html', form=form, form_name='edit store')
    elif request.method == 'POST':

        if form.validate():
            result.store_name = form.store_name.data
            result.store_link = form.store_link.data

            db.session.commit()
            return redirect('/all_store')
        else:
            return render_template('edit_store_form.html', form=form, form_name='edit store')


@app.route('/delete_store/<string:store_name>', methods=['GET', 'POST'])
def delete_store(store_name):
    result = db.session.query(Store).filter(Store.store_name == store_name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/all_store')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = CreateQuery()

    if request.method == 'POST':
        if not form.validate():
            return render_template('Search.html', form=form, form_name="Search", action="search")
        else:
            list_goods.clear()
            list_goods1.clear()
            for id, ids, name, model in db.session.query(Goods.stores, Goods.good_id, Goods.good_name,
                                                         Goods.good_model):
                if name == form.good_name.data and model == form.good_model.data:
                    list_goods.append(id)
                    list_goods1.append(ids)
                    print("dawd",list_goods)
                    print("d", list_goods1)

            return redirect(url_for('searchList'))

    return render_template('search.html', form=form, form_name="Search", action="search")


@app.route('/search/result', methods=['GET', 'POST'])
def searchList():
    que1=[]
    res=[]
    try:
        for i in list_goods:
            name, model = db.session.query(Store.store_name, Store.store_link).filter(Store.store_id == i).one()
            res.append(
                {"name": name, "model": model})
        for j in list_goods1:
            que1 = db.session.query(Charac.charac_name, Charac.charac_description, Charac.goods_fk).filter(Charac.goods_fk == j).all()
            print("id", que1[2])
            print("len", len(que1))
            for i in range(len(que1)):
                nn=que1[i][0]
                dd= que1[i][1]
                res.append({"name_c": nn, "desc": dd})
        print("res",res)
    except:
        print("don't data")
        print(res)
        for item in res:
            print(item)
    return render_template('search_list.html', results=res)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    query1 = (
        db.session.query(
            Goods.good_name,
            func.count(Charac.charac_name).label('charac_name_count')
        ).
            outerjoin(Charac).
            group_by(Goods.good_name)
    ).all()

    name, charac_count = zip(*query1)
    bar = go.Bar(
        x=name,
        y=charac_count
    )
    print(query1)
    query3 = (
        db.session.query(
            func.count(Goods.good_name),
            Store.store_name).group_by(Store.store_name)
        ).all()
    print(query3)
    count_of_name, store = zip(*query3)
    pie = go.Pie(
        labels=store,
        values=count_of_name
    )

    data = {

        "bar": [bar],
        "pie": [pie],

    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', graphsJSON=graphsJSON)



@app.route('/clasteresation', methods=['GET', 'POST'])
def claster():
    df = pd.DataFrame()

    for good_name, store_name in db.session.query(Goods.good_name, Store.store_name).join(Store,
                                                                                      Goods.stores == Store.store_id):
        print(good_name, store_name)
        df = df.append({"good_name": good_name, "store_name": store_name}, ignore_index=True)

    X = pd.get_dummies(data=df)
    print(X)
    count_clasters = len(df['store_name'].unique())
    print(count_clasters)
    kmeans = KMeans(n_clusters=count_clasters, random_state=0).fit(X)
    # print(kmeans)
    count_columns = len(X.columns)
    test_list = [0] * count_columns
    test_list[0] = 1
    test_list[-1] = 1
    print(test_list)
    # print(kmeans.labels_)
    print(kmeans.predict(np.array([test_list])))

    query1 = (
        db.session.query(
            func.count(),
            Store.store_name
        ).group_by(Store.store_name)
    ).all()
    store, store_count = zip(*query1)
    pie = go.Pie(
        labels=store_count,
        values=store
    )
    data = {
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('clasteresation.html', row=kmeans.predict(np.array([test_list]))[0],
                           count_claster=count_clasters, graphsJSON=graphsJSON)


@app.route('/correlation', methods=['GET', 'POST'])
def correlation():
    df = pd.DataFrame()
    for users, count_user, avg_price in db.session.query(Goods.users, func.count(Goods.users), func.avg(Goods.price)).group_by(Goods.users):
        print(count_user, avg_price)
        df = df.append({"count_user": float(count_user), "avg_price": float(avg_price)}, ignore_index=True)
    db.session.close()
    scaler = StandardScaler()
    scaler.fit(df[["count_user"]])
    train_X = scaler.transform(df[["count_user"]])
    # print(train_X, df[["count_files"]])
    reg = LinearRegression().fit(train_X, df[["avg_price"]])

    test_array = [[3]]
    test = scaler.transform(test_array)
    result = reg.predict(test)

    query1 = db.session.query(Goods.users, func.count(Goods.users), func.avg(Goods.price)).group_by(Goods.users).all()
    name, count_pr, count_fl = zip(*query1)
    scatter = go.Scatter(
        x=count_pr,
        y=count_fl,
        mode = 'markers',
        marker_color='rgba(255, 0, 0, 100)',
        name = "data"
    )
    x_line = np.linspace(0, 10)
    y_line = x_line * reg.coef_[0, 0] + reg.intercept_[0]
    line = go.Scatter(
        x=x_line,
        y=y_line,
        mode = 'lines',
        marker_color='rgba(0, 0, 255, 100)',
        name = "regretion"
    )
    data = [scatter, line]
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('regretion.html', row=int(round(result[0, 0])), test_data=test_array[0][0], coef=reg.coef_[0],
                           coef1=reg.intercept_, graphsJSON = graphsJSON)

@app.route('/clasification', methods=['GET', 'POST'])
def clasification():
    df = pd.DataFrame()
    for name, model, price in db.session.query(Goods.good_name, Goods.good_model, Goods.price):
        print(name, model, price)
        df = df.append({"name": name, "model": model, "price": price}, ignore_index=True)
    # db.session.close()

    mean_p = df['price'].mean()
    df.loc[df['price'] < mean_p, 'quality'] = 0
    df.loc[df['price'] >= mean_p, 'quality'] = 1
    X = pd.get_dummies(data=df[['name', 'model']])
    print(df)
    print(X)
    # pnn = algorithms.PNN(std=10, verbose=False)
    pnn = KNeighborsClassifier(2)
    pnn.fit(X, df['quality'])
    test_str= ['Huawei', 'S10']
    count_columns = len(X.columns)
    test_list = [0] * count_columns
    test_list[0] = 1
    test_list[-1] = 1
    print(test_list)
    y_predicted = pnn.predict([test_list])
    result = "Ні"
    if y_predicted - 1 < 0.0000001:
        result = "Так"

    return render_template('clasification.html', y_predicted=result, test_data=test_list, test_str=test_str)


if __name__ == "__main__":
    app.run(debug=True)
