from numpy import sort
from sqlalchemy import asc
from flask import Flask, request, render_template, redirect, url_for
from connecting.credentials import *
from model.model import db, QuestionsTable, QuestionnaireTable, AnswerTable, UniversityUsersTable
from model.fillDBscript import fill_users_script, fill_questions_script, fill_questionnaires_script, fill_answers_script
from forms.AnswerForm import AnswerForm
from forms.QuestionForm import QuestionForm
from forms.QuestionnaireForm import QuestionnaireForm
from forms.LoginForm import LoginForm
from forms.UniversityUsersForm import UniversityUserForm
from model.vizualization import visualization_data
from model.send_email import send_email
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from connecting.db import PostgresDb
import os
from flask_login import login_user, login_required, current_user, logout_user, LoginManager

new_db = PostgresDb()

app = Flask(__name__)
app.secret_key = 'development key'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route("/fill")
def fill():
    fill_users_script()
    fill_questions_script()
    fill_questionnaires_script()
    fill_answers_script()
    db.session.commit()
    return redirect(url_for('login'))


@app.route("/", methods=["GET", "POST"])
def login():
    db.create_all()
    form = LoginForm()
    error = None

    if request.method == "POST":
        if not form.validate():
            return render_template("authentication/index.html", form=form)

        account = UniversityUsersTable.query.filter(UniversityUsersTable.User_email == form.User_email.data).first()
        if account is None:
            error = "Invalid username or password"
        elif account.User_email != "admin@kpi.ua":
            login_user(account)
            redirect_url = request.args.get("next")
            return redirect(redirect_url or url_for("students"))
        else:
            login_user(account)
            redirect_url = request.args.get("next")
            return redirect(redirect_url or url_for("admins"))

    return render_template("authentication/index.html", form=form, error=error)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load(user_id):
    if user_id is not None:
        return UniversityUsersTable.query.get(user_id)
    return None


@app.route("/admins")
@login_required
def admins():
    return render_template("admin_main.html")


@app.route("/admins/students")
@login_required
def admins_students():
    all_students = UniversityUsersTable.query.order_by(asc(UniversityUsersTable.User_email)).all()
    return render_template("admins/students/index.html", users=all_students)


@app.route("/admins/students/new", methods=["GET", "POST"])
@login_required
def admins_new_student():
    form = UniversityUserForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("admins/students/create.html", form=form)
        else:
            student = form.model()
            db.session.add(student)
            db.session.commit()
            return redirect(url_for("admins_students"))

    return render_template("admins/students/create.html", form=form)


@app.route("/admins/students/delete/<uuid>", methods=["POST"])
@login_required
def admins_delete_student(uuid):
    student = UniversityUsersTable.query.filter(UniversityUsersTable.User_email == uuid).first()
    if student:
        db.session.delete(student)
        db.session.commit()

    return redirect(url_for("admins_students"))


@app.route("/admins/students/<uuid>", methods=["GET", "POST"])
@login_required
def admins_update_student(uuid):
    student = UniversityUsersTable.query.filter(UniversityUsersTable.User_email == uuid).first()
    form = student.filled_form()

    if request.method == "POST":
        if not form.validate():
            return render_template("admins/students/update.html", form=form)

        student.map_to_form(form)
        db.session.commit()
        return redirect(url_for("admins_students"))

    return render_template("admins/students/update.html", form=form)


@app.route("/admins/questionnaires")
@login_required
def admins_questionnaires():
    all_questionnaires = QuestionnaireTable.query.join(QuestionsTable).order_by(
        asc(QuestionnaireTable.Questionnaire_id)).all()
    return render_template("admins/questionnaires/index.html", questionnaires=all_questionnaires)


@app.route("/admins/questionnaires/new", methods=["GET", "POST"])
@login_required
def admins_new_questionnaire():
    form = QuestionnaireForm()
    form.Questions.choices = [
        (str(question.Question_id), f"{question.Questions} (Type is: {question.Type_question})") for question in
        QuestionsTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("admins/questionnaires/create.html", form=form)
        else:
            questionnaire = form.model()
            db.session.add(questionnaire)
            db.session.commit()
            return redirect(url_for("admins_questionnaires"))

    return render_template("admins/questionnaires/create.html", form=form)


@app.route("/admins/questionnaires/delete/<uuid>", methods=["POST"])
@login_required
def admins_delete_questionnaire(uuid):
    questionnaire = QuestionnaireTable.query.filter(QuestionnaireTable.Questionnaire_id == uuid).first()
    if questionnaire:
        db.session.delete(questionnaire)
        db.session.commit()

    return redirect(url_for("admins_questionnaires"))


@app.route("/admins/questionnaires/<uuid>", methods=["GET", "POST"])
@login_required
def admins_update_questionnaire(uuid):
    questionnaire = QuestionnaireTable.query.filter(QuestionnaireTable.Questionnaire_id == uuid).first()
    form = questionnaire.filled_form()
    form.Questions.choices = [(str(question.Question_id), question.Questions) for question in
                              QuestionsTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("admins/questionnaires/update.html", form=form)

        questionnaire.map_to_form(form)
        db.session.commit()
        return redirect(url_for("admins_questionnaires"))

    return render_template("admins/questionnaires/update.html", form=form)


@app.route("/admins/answers")
@login_required
def admins_answers():
    all_answers = AnswerTable.query.join(QuestionsTable).join(UniversityUsersTable).order_by(
        asc(AnswerTable.Answer_id)).all()
    return render_template("admins/answers/index.html", answers=all_answers)


@app.route("/admins/questions")
@login_required
def admins_questions():
    all_questions = QuestionsTable.query.order_by(asc(QuestionsTable.Question_id)).all()
    return render_template("admins/questions/index.html", questions=all_questions)


@app.route("/admins/questions/new", methods=["GET", "POST"])
@login_required
def admins_new_question():
    form = QuestionForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("admins/questions/create.html", form=form)
        else:
            question = form.model()
            db.session.add(question)
            db.session.commit()
            return redirect(url_for("admins_questions"))

    return render_template("admins/questions/create.html", form=form)


@app.route("/admins/questions/delete/<uuid>", methods=["POST"])
@login_required
def admins_delete_question(uuid):
    question = QuestionsTable.query.filter(QuestionsTable.Question_id == uuid).first()
    if question:
        db.session.delete(question)
        db.session.commit()

    return redirect(url_for("admins_questions"))


@app.route("/admins/questions/<uuid>", methods=["GET", "POST"])
@login_required
def admins_update_question(uuid):
    question = QuestionsTable.query.filter(QuestionsTable.Question_id == uuid).first()
    form = question.filled_form()

    if request.method == "POST":
        if not form.validate():
            return render_template("admins/questions/update.html", form=form)

        question.map_to_form(form)
        db.session.commit()
        return redirect(url_for("admins_questions"))

    return render_template("admins/questions/update.html", form=form)


@app.route("/students")
@login_required
def students():
    return render_template("main.html")


@app.route("/students/answers")
@login_required
def answers():
    all_answers = AnswerTable.query.join(QuestionsTable).join(UniversityUsersTable).order_by(
        asc(AnswerTable.Answer_id)).all()
    return render_template("students/answers/index.html", answers=all_answers)


@app.route("/students/answers/new", methods=["GET", "POST"])
@login_required
def new_answer():
    form = AnswerForm()
    form.Questions.choices = [(str(question.Question_id), question.Questions) for question in
                              QuestionsTable.query.all()]
    form.Student_answer.choices = [(str(current_user.User_email), student.UserFullName) for student in
                                   UniversityUsersTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("students/answers/create.html", form=form)
        else:
            answer = form.model()
            db.session.add(answer)
            db.session.commit()
            send_email(form.Answer_for_question, form.Questions, form.Student_answer, form.User_faculty,
                       current_user.User_email)
            return redirect(url_for("answers"))

    return render_template("students/answers/create.html", form=form)


@app.route("/students/answers/delete/<uuid>", methods=["POST"])
@login_required
def delete_answer(uuid):
    answer = AnswerTable.query.filter(AnswerTable.Answer_id == uuid).first()
    if answer:
        db.session.delete(answer)
        db.session.commit()

    return redirect(url_for("answers"))


@app.route("/students/answers/<uuid>", methods=["GET", "POST"])
@login_required
def update_answer(uuid):
    answer = AnswerTable.query.filter(AnswerTable.Answer_id == uuid).first()
    form = answer.filled_form()
    form.Questions.choices = [(str(question.Question_id), question.Questions) for question in
                              QuestionsTable.query.all()]
    form.Student_answer.choices = [(str(student.User_email), student.UserFullName) for student in
                                   UniversityUsersTable.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("students/answers/update.html", form=form)

        answer.map_to_form(form)
        db.session.commit()
        return redirect(url_for("answers"))

    return render_template("students/answers/update.html", form=form)


@app.route("/students/questionnaires")
@login_required
def questionnaires():
    all_questionnaires = QuestionnaireTable.query.join(QuestionsTable).order_by(
        asc(QuestionnaireTable.Questionnaire_id)).all()
    return render_template("students/questionnaires/index.html", questionnaires=all_questionnaires)


@app.route("/admins/bar", methods=["GET"])
def visualization():
    data = visualization_data()

    return render_template("admins/bar.html", students_cars=data)


@app.route("/admins/predictions", methods=['GET', 'POST'])
def predict():
    new_db = PostgresDb()
    QuestionnaireID = []
    QuestionID = []
    result = new_db.sqlalchemy_session.query(QuestionnaireTable).all()
    for row in result:
        QuestionnaireID.append(row.Questionnaire_id)
        QuestionID.append(row.QuestionIdFk)

    X = pd.DataFrame(list(zip(QuestionnaireID, QuestionID)),
                     columns=['Questions', 'Type_question'])

    y = pd.DataFrame(QuestionID)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    regressor = RandomForestRegressor(n_estimators=200, random_state=0)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    y_pred_sort = sort(y_pred)

    filename = 'finalized_model.pkl'
    pickle.dump(regressor, open(filename, 'wb'))

    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.score(X_test, y_test)
    if len(y_pred_sort) == 1:
        return render_template("admins/predictions/predict1.html", result=y_pred_sort)
    elif len(y_pred_sort) == 2:
        return render_template("admins/predictions/predict2.html", result=y_pred_sort)
    elif len(y_pred_sort) == 3:
        return render_template("admins/predictions/predict3.html", result=y_pred_sort)


if __name__ == "__main__":
    app.run(debug=True)
