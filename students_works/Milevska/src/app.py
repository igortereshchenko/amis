
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_session import Session
from flask_wtf import CSRFProtect

from forms.forms import TestForm, QuestionForm, QuestionVariantForm, SignupForm, UserUpdateForm
from dao.orm.model import *
from dao.db import PostgresDB
from sqlalchemy.sql import func
from forms.forms import LoginForm
from flask_weasyprint import render_pdf, HTML
import plotly
import plotly.graph_objs as go

from neural_network_model.classify.classify import get_weights, get_best_discipline
from neural_network_model.clustering.generate_clusters import clustering_axes
import json

login_manager = LoginManager()
sess = Session()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'faFFAshfuhuhf1u2heu1heqwdas'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager.init_app(app)
sess.init_app(app)

csrf = CSRFProtect(app)
db = PostgresDB()


@app.route('/', methods=['GET', 'POST'])
def root():
    users = db.sqlalchemy_session.query(ormUser).all()
    return render_template('index.html', users=users)


@app.route('/test', methods=['GET'])
def test():

    result = db.sqlalchemy_session.query(ormTest).all()

    return render_template('test.html', tests=result)


@app.route('/test', methods=['POST'])
def create_test():
    form = TestForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        db.sqlalchemy_session.add(ormTest(test_name=data.get('test_name'), test_variant=int(data.get('test_variant'))))
        db.sqlalchemy_session.commit()
    return redirect('/test')


@app.route('/test/<id>', methods=['POST'])
def update_test(id):
    form = TestForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        test = db.sqlalchemy_session.query(ormTest).filter(ormTest.test_id == id).first()
        if test:
            test.test_name = data.get('test_name', test.test_name)
            test.test_variant = data.get('test_variant', test.test_variant)
            db.sqlalchemy_session.commit()
            return redirect('/test')
        else:
            return 404


@app.route('/test/<id>/delete', methods=['GET', ])
def delete_test(id):
    test = db.sqlalchemy_session.query(ormTest).filter(ormTest.test_id == id).first()
    db.sqlalchemy_session.delete(test)
    return redirect('/test')


@app.route('/questions', methods=['GET'])
def questions():

    result = db.sqlalchemy_session.query(ormTest).all()
    disciplines = db.sqlalchemy_session.query(ormDiscipline).all()
    return render_template('questions.html', tests=result, disciplines=disciplines)


@app.route('/question', methods=['POST'])
def create_question():
    form = QuestionForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        discipline_id = int(data.get('discipline_id')) if data.get('discipline_id', None) else None
        db.sqlalchemy_session.add(
            ormQuestion(
                question_text=data.get('question_text'),
                test_id=int(data.get('test_id')),
                discipline_id=discipline_id
            )
        )
        db.sqlalchemy_session.commit()
        return redirect('/questions')
    else:
        return 'errors'


@app.route('/question/<id>', methods=['POST'])
def update_question(id):
    form = QuestionForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        question = db.sqlalchemy_session.query(ormQuestion).filter(ormQuestion.question_id == id).first()
        if question:
            question.question_text = data.get('question_text', question.question_text)
            question.discipline_id = data.get('discipline_id', question.discipline_id)
            db.sqlalchemy_session.commit()
            return redirect(url_for('questions'))
        else:
            return 'errors'


@app.route('/question/<id>/delete', methods=['GET', ])
def delete_question(id):
    question = db.sqlalchemy_session.query(ormQuestion).filter(ormQuestion.question_id == id).first()
    db.sqlalchemy_session.delete(question)
    return redirect('/questions')


@app.route('/answer_variants', methods=['GET'])
def answer_variants():

    result = db.sqlalchemy_session.query(ormQuestion).all()

    return render_template('answer_variants.html', questions=result)


@app.route('/question_variant', methods=['POST'])
def create_question_variant():
    form = QuestionVariantForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        db.sqlalchemy_session.add(ormAnswerVariant(answer_variant_text=data.get('answer_variant_text'), question_id=int(data.get('question_id'))))
        db.sqlalchemy_session.commit()
        return redirect('/answer_variants')
    else:
        return 'errors'


@app.route('/question_variant/<id>', methods=['POST'])
def update_answer_variant(id):
    form = QuestionVariantForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        answer_variant = db.sqlalchemy_session.query(ormAnswerVariant).filter(ormAnswerVariant.answer_variant_id == id).first()
        if answer_variant:
            answer_variant.answer_variant_text = data.get('answer_variant_text', answer_variant.answer_variant_text)
            db.sqlalchemy_session.commit()
            return redirect('/answer_variants')
        else:
            return 'errors'


@app.route('/answer_variants/<id>/delete', methods=['GET', ])
def delete_answer_variants(id):
    db.sqlalchemy_session.query(ormAnswerVariant).filter(ormAnswerVariant.answer_variant_id == id).delete(synchronize_session='evaluate')
    db.sqlalchemy_session.commit()
    return redirect('/answer_variants')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    pies = []
    bars = []
    query1 = db.sqlalchemy_session.query(
        ormDiscipline.name,
        func.count(ormDiscipline.questions).label('discipline_questios_count')
    ).outerjoin(ormQuestion).group_by(
        ormDiscipline.name
    )

    query2 = db.sqlalchemy_session.query(
        ormTest.test_name,
        func.count(ormQuestion.question_id).label('question_count')
    ).outerjoin(ormQuestion).group_by(ormTest.test_name).all()

    variants, question_counts = zip(*query1)
    bar = go.Bar(
        x=variants,
        y=question_counts
    )
    bars.append(bar)

    tests, question_count = zip(*query2)
    pie = go.Pie(
        labels=tests,
        values=question_count
    )
    pies.append(pie)

    data = {
        "bar": bars,
        "pie": pies
    }
    graphsJSON = json.dumps(
        data,
        cls=plotly.utils.PlotlyJSONEncoder
    )

    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    # Bypass Login screen if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('root'))
    login_form = LoginForm(request.form)
    # POST: Create user and redirect them to the app
    if request.method == 'POST':
        if login_form.validate():
            # Get Form Fields
            email = request.form.get('email')
            password = request.form.get('password')
            # Validate Login Attempt
            user = db.sqlalchemy_session.query(ormUser).filter_by(email=email).first()
            if user:
                if user.check_password(password=password):
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('root'))
        flash('Invalid username/password combination')
        return redirect(url_for('login'))
    # GET: Serve Log-in page
    return render_template('login.html',
                           form=LoginForm(),
                           title='Log in | Flask-Login Tutorial.',
                           template='login-page',
                           body="Log in with your User account.")


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return db.sqlalchemy_session.query(ormUser).get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


@app.route("/logout", methods=['GET',])
@login_required
def logout_page():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User sign-up page."""
    signup_form = SignupForm(request.form)
    # POST: Sign user in
    if request.method == 'POST':
        if signup_form.validate():
            # Get Form Fields
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            existing_user = db.sqlalchemy_session.query(ormUser).filter_by(email=email).first()
            if existing_user is None:
                user = ormUser(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    role='STANDARD'
                )
                db.sqlalchemy_session.add(user)
                db.sqlalchemy_session.commit()
                login_user(user)
                return redirect(url_for('root'))
            flash('A user already exists with that email address.')
            return redirect(url_for('register'))
    return render_template('register.html',
                           title='Create an Account | Flask-Login Tutorial.',
                           form=signup_form,
                           template='signup-page',
                           body="Sign up for a user account.")


@app.route('/users/<id>/update', methods=['POST',])
def update_user(id):
    form = UserUpdateForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        user = db.sqlalchemy_session.query(ormUser).filter(ormUser.id == id).first()
        if user:
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.role = data.get('role', user.role)
            db.sqlalchemy_session.commit()
            return redirect(url_for('root'))
        else:
            return redirect(url_for('root'))


@app.route('/users/<id>/delete', methods=['GET',])
def delete_user(id):
    user = db.sqlalchemy_session.query(ormUser).filter(ormUser.id == id).first()
    db.sqlalchemy_session.delete(user)
    return redirect(url_for('root'))


@app.route('/test_<id>.pdf')
def test_to_pdf(id):
    test = db.sqlalchemy_session.query(ormTest).filter(ormTest.test_id == id).first()
    html = render_template('test_pdf_template.html', test=test)
    return render_pdf(HTML(string=html))


@app.route('/questions/<id>/define_discipline')
def define_discipline(id):
    question = db.sqlalchemy_session.query(ormQuestion).filter(ormQuestion.question_id == id).first()
    if not question:
        return redirect(url_for('questions'))
    discipline_name = get_best_discipline(question.question_text)
    discipline = db.sqlalchemy_session.query(ormDiscipline).filter(ormDiscipline.name == discipline_name).first()
    if discipline:
        question.discipline_id = discipline.id
        db.sqlalchemy_session.commit()
    return redirect(url_for('questions'))


@app.route('/statistics')
def statistics():
    x, y, z = clustering_axes()

    disciplines = db.sqlalchemy_session.query(ormDiscipline).all()

    disc_first = request.args.get('disc_first')
    disc_second = request.args.get('disc_second')
    x_first_cor = []
    y_first_cor = []

    x_second_cor = []
    y_second_cor = []

    if disc_first and disc_second:
        corr_array = get_weights('neural_network_model/classify/synapses_short.json')[0]
        y_first_cor = [item[int(disc_first)] for item in corr_array[:1000]]
        x_first_cor = [i for i in range(1, len(y_first_cor))]

        y_second_cor = [item[int(disc_second)] for item in corr_array[:1000]]
        x_second_cor = x_first_cor

    return render_template(
        'statistics.html',
        x=list(x),
        y=list(y),
        z=list(z),
        disciplines=disciplines,
        x_first_cor=list(x_first_cor),
        y_first_cor=list(y_first_cor),
        x_second_cor=list(x_second_cor),
        y_second_cor=list(y_second_cor),
        disc_first=disc_first,
        disc_second=disc_second
    )


if __name__ == '__main__':
    app.run(debug=True)
