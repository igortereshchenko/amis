import json

import numpy
import pandas
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.ext.declarative import declarative_base

from dao.db import PostgresDb
from dao import credentials
from dao.db import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, func, select, join
from sqlalchemy.orm import relationship

from dao.orm.model import *
from dao.db import PostgresDb
from dao.credentials import *

import plotly
import plotly.graph_objects as go

from forms.AlbumForm import AlbumForm
from forms.MelodyForm import MelodyForm
from forms.Search_psychotype import SearchPsychForm

db = PostgresDb()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jkm-vsnej9l-vm9sqm3:lmve")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{host}:{port}/{database}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/new_album')
def new_album():
    form = AlbumForm()
    return render_template("new_album.html", form = form, action="new_album", form_name = "New album")

@app.route('/new_melody')
def new_melody():
    form = MelodyForm()
    return render_template("new_melody.html", form = form, action="new_melody", form_name = "New melody")

@app.route('/try', methods=['POST', 'GET'])
def some_query():
    #result=db.sqlalchemy_session.query(student).join(wish).join(melody).join(genre).filter(student.id==wish.student_id
    #and wish.wish_melody==melody.id and melody.melody_genre==genre.id)
    #result = db.sqlalchemy_session.query(student).join(wish, student.id==wish.student_id).join(melody, wish.wish_melody==melody.id).\
    #    join(genre, melody.melody_genre==genre.id).all()

    #result=db.sqlalchemy_session.query(student.faculty, genre.psychotype, func.count(genre.psychotype)).filter(student.id==wish.student_id and wish.wish_melody==melody.id
    #                                                                       and melody.melody_genre==genre.id).group_by(student.faculty, genre.psychotype)

    # result = db.sqlalchemy_session.query(student.faculty, genre.psychotype, func.count(genre.psychotype)).filter(
    #     student.id == wish.student_id and wish.wish_melody == melody.id and melody.melody_genre==genre.id).\
    #     group_by(student.faculty, genre.psychotype).subquery()
    #
    # result2=db.sqlalchemy_session.query(result.c.psychotype).filter(result.c.faculty=='FICT')
    form = SearchPsychForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("search_by_facul.html", form=form, action="try", form_name="searchps")
        else:
            fac_parameter = form.faculty.data

            result2 = db.sqlalchemy_session.query(genre.psychotype, func.count(genre.psychotype)).join(melody, melody.melody_genre==genre.id).\
                join(wish, wish.wish_melody==melody.id).join(student, student.id==wish.student_id).filter(student.faculty==fac_parameter).\
                group_by(student.faculty, genre.psychotype)
            # psychotypes = list(result2)
            for row in result2:
                print(row)
            psychotypes = dict((genre, count) for genre, count in result2)
            print(psychotypes)
            psychotypes_invert = dict((count, genre) for genre, count in result2)
            print(psychotypes_invert)
            maxkey = psychotypes_invert[max(psychotypes.values())]
            print(max(psychotypes.values()), 'and its key ', maxkey)

            #result3 = db.sqlalchemy_session.query(result2.c.psychotype)
            # mass = []
            # for i in range(len(psychotypes)):
            #     mass.append(psychotypes[i][0])
            #print(result2)

            # j = join(user_table, address_table,
            #          user_table.c.id == address_table.c.user_id)
            # stmt = select([user_table]).select_from(j)
            # j = join(student, wish, melody, genre, student.id == wish.student_id, wish.wish_melody == melody.id, melody.melody_genre==genre.id)
            #     # query = select([genre.psychotype]).select_from(select([student.faculty, genre.psychotype]).select_from(j)).where(student.faculty=='FICT')
            #     # print(query)
            #     # result = db.sqlalchemy_session.execute(query)
            #     # for row in result:
            #     #     print(row)
            # big_join = db.sqlalchemy_session.query(student, wish, genre, melody).filter(
            #      student.id == wish.student_id and wish.wish_melody == melody.id and melody.melody_genre==genre.id)
            # print(big_join)
            return "<h1>success</h1>"

    return render_template("search_by_facul.html", form=form, action="try", form_name="searchps")

def create_graph():
    # x=[]
    # y=[]
    # names = list(db.sqlalchemy_session.query(ormGanre.name))
    # #print(names[0][0])
    # subs = list(db.sqlalchemy_session.query(ormGanre.count_of_subscribers))
    # #df = pandas.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
    # for i in range(len(names)):
    #     x.append(names[i][0])
    # for i in range(len(subs)):
    #     y.append(int(subs[i][0]))
    # print(x)
    # print(y)
    # data = [
    #     go.Bar(
    #         x=x,  # assign x as the dataframe column 'x'
    #         y=y
    #     )
    # ]

    # labels = ['Oxygen', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen']
    # values = [4500, 2500, 1053, 500]
    #
    # fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    N = 1000
    t = numpy.linspace(0, 10, 100)
    y = numpy.sin(t)

    fig = go.Figure(data=go.Scatter(x=t, y=y, mode='markers'))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/gr', methods=['GET', 'POST'])
def draw_graph():
    bar = create_graph()
    return render_template('graphics.html', plot=bar)

if __name__ == '__main__':
    app.run()
