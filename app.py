import json
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from dao.orm.model import *
from dao.db import PostgresDb
from dao.credentials import *
import plotly
import plotly.graph_objects as go
from forms.AlbumForm import AlbumForm
from forms.GenreForm import GenreForm
from forms.MelodyForm import MelodyForm
from forms.PerformerForm import PerformerForm
from forms.Search_psychotype import SearchPsychForm
from forms.StudentForm import StudentForm
from forms.WishForm import WishForm

db = PostgresDb()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jkm-vsnej9l-vm9sqm3:lmve")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  'postgres://xujoczxbviwzjo:83a4ab01c63234f37abb82fabf8294c7f26494fdd92b567ead595ea821a3abba@ec2-174-129-24-148.compute-1.amazonaws.com:5432/dbriles54vm09o')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template("index.html")

@app.route('/show_tables', methods=['GET', 'POST'])
def show_tables():
    students = db.sqlalchemy_session.query(student).all()
    genres = db.sqlalchemy_session.query(genre).all()
    performers = db.sqlalchemy_session.query(performer).all()
    albums = db.sqlalchemy_session.query(album.title, performer.name).join(performer, performer.id==album.performer_id).all()
    melodies = db.sqlalchemy_session.query(melody.title, melody.singer, melody.release_date, genre.name, album.title.label("albumtitle")).\
        join(genre, genre.id==melody.melody_genre).join(album, melody.album_id==album.id).all()
    wishes = db.sqlalchemy_session.query(student.surname, wish.wish_date, performer.name, melody.title, genre.name.label("genrename")).\
       join(wish, student.id==wish.student_id).join(melody, wish.wish_melody==melody.id).join(genre, genre.id==melody.melody_genre).\
       join(album, album.id==melody.album_id).join(performer, performer.id==album.performer_id).all()
    #wishes = db.sqlalchemy_session.query(wish).all()

    return render_template("tables.html", students=students, genres=genres,
                           performers=performers, albums=albums, melodies=melodies, wishes=wishes)

@app.route('/new_album', methods=['GET', 'POST'])
def new_album():
    form = AlbumForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_album.html', form=form, form_name="Новий альбом", action="new_album")
        else:
            album_id = list(db.sqlalchemy_session.query(func.max(album.id)))[0][0]
            album_obj = album(
                id= album_id + 1,
                title=form.album_name.data,
                performer_id=form.album_performer.data
                )

            db.sqlalchemy_session.add(album_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('show_tables'))

    return render_template("new_album.html", form = form, action="new_album", form_name = "Новий альбом")

@app.route('/new_melody', methods=['GET', 'POST'])
def new_melody():
    form = MelodyForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_melody.html', form=form, form_name="Нова мелодія", action="new_melody")
        else:
            melody_id = list(db.sqlalchemy_session.query(func.max(melody.id)))[0][0]
            melody_obj = melody(
                id = melody_id+1,
                title = form.title.data,
                singer = form.singer.data,
                release_date =form.release_date.data,
                melody_genre = form.melody_genre.data,
                album_id = form.album_id.data
                )

            db.sqlalchemy_session.add(melody_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('show_tables'))
    return render_template("new_melody.html", form = form, action="new_melody", form_name = "Нова мелодія")

@app.route('/new_performer', methods=['GET', 'POST'])
def new_performer():
    form = PerformerForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_performer.html', form=form, form_name="Новий виконавець", action="new_performer")
        else:
            performer_id = list(db.sqlalchemy_session.query(func.max(performer.id)))[0][0]
            performer_obj = performer(
                id= performer_id + 1,
                name = form.name.data
                )

            db.sqlalchemy_session.add(performer_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('show_tables'))
    return render_template("new_performer.html", form = form, action= "new_performer", form_name = "Новий виконавець")

@app.route('/new_genre', methods=['GET', 'POST'])
def new_genre():
    form = GenreForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_genre.html', form=form, form_name="Новий виконавець", action="new_genre")
        else:
            genre_id = list(db.sqlalchemy_session.query(func.max(genre.id)))[0][0]
            genre_obj = genre(
                id= genre_id + 1,
                name = form.genre_name.data,
                psychotype=form.psychotype.data
                )

            db.sqlalchemy_session.add(genre_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('show_tables'))
    return render_template("new_genre.html", form = form, action= "new_genre", form_name = "Новий жанр")

@app.route('/edit_genre', methods=['GET', 'POST'])
def edit_genre():
    form = GenreForm()

    if request.method == 'GET':

        id = request.args.get('id')

        db = PostgresDb()
        genre_obj = db.sqlalchemy_session.query(genre).filter(genre.id == id).one()

        # fill form and send to user
        form.id.data = genre_obj.id
        form.genre_name.data = genre_obj.name
        form.psychotype.data = genre_obj.psychotype

        return render_template('new_genre.html', form=form, form_name="Редагувати інформацію про жанр", action="edit_genre")

    else:
        if not form.validate():
            return render_template('new_genre.html', form=form, form_name="Редагувати інформацію про жанр", action="edit_genre")
        else:
            db = PostgresDb()
            # find professor
            genre_obj = db.sqlalchemy_session.query(genre).filter(genre.id == form.id.data).one()

            # update fields from form data
            genre_obj.id = form.id.data
            genre_obj.name = form.genre_name.data
            genre_obj.psychotype = form.psychotype.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('show_tables'))

@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    form = StudentForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('new_student.html', form=form, form_name="Новий студент", action="new_student")
        else:
            student_id = list(db.sqlalchemy_session.query(func.max(student.id)))[0][0]
            student_obj = student(
                id=student_id + 1,
                faculty=form.faculty.data,
                group=form.group.data,
                name=form.name.data,
                surname=form.surname.data,
                username=form.username.data)

            db.sqlalchemy_session.add(student_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('show_tables'))
    return render_template("new_student.html", form = form, action= "new_student", form_name = "Новий студент")

@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    form = StudentForm()
    db = PostgresDb()
    if request.method == 'GET':

        id = request.args.get('id')

        student_obj = db.sqlalchemy_session.query(student).filter(student.id == id).one()

        # fill form and send to user
        form.id.data = student_obj.id
        form.faculty.data = student_obj.faculty
        form.group.data = student_obj.group
        form.name.data = student_obj.name
        form.surname.data = student_obj.surname
        form.username.data = student_obj.username

        return render_template('new_student.html', form=form, form_name="Редагувати інформацію про студента", action="edit_student")

    else:
        if not form.validate():
            return render_template('new_student.html', form=form, form_name="Редагувати інформацію про студента", action="edit_student")
        else:
            db = PostgresDb()
            # find professor
            student_obj = db.sqlalchemy_session.query(student).filter(student.id == form.id.data).one()

            # update fields from form data
            student_obj.id = form.id.data
            student_obj.faculty = form.faculty.data
            student_obj.group = form.group.data
            student_obj.name = form.name.data
            student_obj.surname = form.surname.data
            student_obj.username = form.username.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('show_tables'))

@app.route('/delete_student')
def delete_student():
    student_id = request.args.get('id')

    result = db.sqlalchemy_session.query(student).filter(student.id == student_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('show_tables'))

@app.route('/new_wish', methods=['GET', 'POST'] )
def new_wish():
    form = WishForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_wish.html', form=form, form_name="Нове побажання", action="new_wish")
        else:
            wish_id = list(db.sqlalchemy_session.query(func.max(wish.id)))[0][0]
            wish_obj = wish(
                id=wish_id + 1,
                student_id = form.student_id.data,
                wish_date = form.wish_date.data,
                wish_performer = form.wish_performer.data,
                wish_melody = form.wish_melody.data,
                wish_genre = form.wish_genre.data
            )

            db.sqlalchemy_session.add(wish_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('show_tables'))
    return render_template("new_wish.html", form = form, action= "new_wish", form_name = "Нове побажання")

@app.route('/try', methods=['POST', 'GET'])
def some_query():
    form = SearchPsychForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("search_by_facul.html", form=form, action="try", form_name="Визначити психотип студентів факультету")
        else:
            fac_parameter = form.fac.data
            print(fac_parameter)
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

            x = []
            y = []
            for a in psychotypes.keys():
                x.append(a)
            for b in psychotypes.values():
                y.append(b)

            print(x)
            print(y)
            data = [
                go.Bar(
                    x=x,  # assign x as the dataframe column 'x'
                    y=y
                )
            ]

            graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

            bar = graphJSON
            return render_template('graphics.html', plot=bar)

    return render_template("search_by_facul.html", form=form, action="try", form_name="Визначити психотип студентів факультету")

# def create_graph():
#     x = []
#     y = []
#     names = list(db.sqlalchemy_session.query(student.faculty))
#     #print(names[0][0])
#     subs = list(db.sqlalchemy_session.query(student.id))
#     #df = pandas.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
#     for i in range(len(names)):
#         x.append(names[i][0])
#     for i in range(len(subs)):
#         y.append(int(subs[i][0]))
#     print(x)
#     print(y)
#     data = [
#         go.Bar(
#             x=x,  # assign x as the dataframe column 'x'
#             y=y
#         )
#     ]
#
#     graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#
#     return graphJSON
#
# @app.route('/gr', methods=['GET', 'POST'])
# def draw_graph():
#     bar = create_graph()
#     return render_template('graphics.html', plot=bar)

# if __name__ == '__main__':
#     app.run()
