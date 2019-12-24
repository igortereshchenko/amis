from flask import Flask, request, render_template, redirect, url_for, abort, jsonify
from domain.models import db, Schemas, Entities, Attributes, Users
from domain.seed import seed
from domain.credentials import *
from forms.schemas import SchemaForm
from forms.entities import EntityForm
from forms.attributes import AttributeViewModel
from forms.dashboard import DashboardViewModel
from forms.auth import LoginViewModel, SignUpViewModel
from views.StatisticsViewModel import StatisticsViewModel
from views.SchemaViewModel import SchemaViewModel
from views.EntityViewModel import EntityViewModel
from views.EntityModifyViewModel import EntityModifyViewModel
from services.analysis import correlation, classification
from services.visualization import schema_distribution_pie, entity_attributes_population_bar
from sqlalchemy import desc
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
import os
import hashlib
import json

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jkm-vsnej9l-vm9sqm3:lmve")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{host}:{port}/{database}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginViewModel()
    error = None

    if request.method == "POST":
        if not form.validate():
            return render_template("authentication/login.html", form=form,
                                   error=form.errors[list(form.errors.keys())[0]])

        user = Users.query.filter(Users.Username == form.Username.data).first()
        if user is None or user.Password != hashlib.sha256(form.Password.data.encode()).hexdigest():
            error = "Invalid username or password"
        else:
            login_user(user)
            redirect_url = request.args.get("next")
            return redirect(redirect_url or url_for("schemas"))

    return render_template("authentication/login.html", form=form, error=error)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpViewModel()
    error = None

    if request.method == "POST":
        if not form.validate():
            return render_template("authentication/signup.html", form=form,
                                   error=form.errors[list(form.errors.keys())[0]][0])

        user = Users.query.filter(Users.Username == form.Username.data).first()
        if user:
            error = "Username already used"
        else:
            new_user = form.domain()
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template("authentication/signup.html", form=form, error=error)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load(user_id):
    if user_id is not None:
        return Users.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route("/db_create")
def db_create():
    db.create_all()
    return "Database created"


@app.route("/seed")
def db_seed():
    # db.create_all()
    seed()
    return "Database populated"


@app.route('/')
@app.route("/schemas")
@login_required
def schemas():
    all_schemas = Schemas.query.filter(Schemas.CreatedByFK == current_user.Username).order_by(
        desc(Schemas.CreatedOn)).all()
    return render_template("schemas/index.html", schemas=all_schemas)


@app.route("/schemas/new", methods=["GET", "POST"])
@login_required
def new_schema():
    form = SchemaForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("schemas/create.html", form=form)
        else:
            schema = form.domain()
            schema.CreatedBy = current_user

            db.session.add(schema)
            db.session.commit()
            return redirect(url_for("schema_info", uuid=schema.Id))

    return render_template("schemas/create.html", form=form)


@app.route("/schemas/delete/<uuid>", methods=["POST"])
@login_required
def delete_schema(uuid):
    schema = Schemas.query.filter(Schemas.Id == uuid and Schemas.CreatedByFk == current_user.Username).first()
    if schema:
        db.session.delete(schema)
        db.session.commit()

    return redirect(url_for("schemas"))


@app.route("/schemas/<uuid>/information", methods=["GET", "POST"])
@login_required
def schema_info(uuid):
    schema = Schemas.query.filter(Schemas.Id == uuid and Schemas.CreatedByFk == current_user.Username).first()

    if not schema:
        abort(404)

    schema_entities = Entities.query.filter(Entities.SchemaIdFk == schema.Id).all() or []

    view = SchemaViewModel(schema, schema_entities)

    return render_template("schemas/information.html", view=view)


@app.route("/schemas/<uuid>/update", methods=["GET", "POST"])
@login_required
def update_schema(uuid):
    schema = Schemas.query.filter(Schemas.Id == uuid and Schemas.CreatedByFk == current_user.Username).first()
    if not schema:
        abort(404)

    form = schema.wtf()

    if request.method == "POST":
        if not form.validate():
            return render_template("schemas/update.html", form=form)

        schema.map_from(form)
        db.session.commit()
        return redirect(url_for("schema_info", uuid=schema.Id))

    return render_template("schemas/update.html", form=form)


@app.route("/entities/<uuid>/information", methods=["GET", "POST"])
@login_required
def entity_info(uuid):
    entity = Entities.query.filter(Entities.Id == uuid).first()
    if not entity:
        abort(404)

    schema = Schemas.query.filter(
        Schemas.Id == entity.SchemaIdFk and Schemas.CreatedByFK == current_user.Username).first()
    if not entity:
        abort(404)

    entity_attributes = Attributes.query.filter(Attributes.EntityIdFk == entity.Id).all() or []

    view = EntityViewModel(schema, entity, entity_attributes)

    return render_template("entities/information.html", view=view)


@app.route("/schemas/<uuid>/entities/new", methods=["GET", "POST"])
@login_required
def new_entity(uuid):
    schema = Schemas.query.filter(Schemas.Id == uuid and Schemas.CreatedByFk == current_user.Username).first()
    if not schema:
        abort(404)

    form = EntityForm()
    view = EntityModifyViewModel(form, schema)

    if request.method == "POST":
        if not form.validate():
            return render_template("entities/create.html", view=view)
        else:
            entity = form.domain()
            entity.Schema = schema
            db.session.add(entity)
            db.session.commit()
            return redirect(url_for("entity_info", uuid=entity.Id))

    return render_template("entities/create.html", view=view)


@app.route("/entities/delete/<uuid>", methods=["POST"])
@login_required
def delete_entity(uuid):
    entity = Entities.query.filter(Entities.Id == uuid).first()
    if entity:
        db.session.delete(entity)
        db.session.commit()

    return redirect(url_for("schema_info", uuid=entity.SchemaIdFk))


@app.route("/entities/<uuid>/update", methods=["GET", "POST"])
@login_required
def update_entity(uuid):
    entity = Entities.query.filter(Entities.Id == uuid).first()

    if not entity:
        abort(404)

    form = entity.wtf()

    if request.method == "POST":
        if not form.validate():
            return render_template("entities/update.html", form=form)
        entity.map_from(form)
        db.session.commit()
        return redirect(url_for("entity_info", uuid=uuid))

    return render_template("entities/update.html", form=form)


@app.route("/entities/<uuid>/attributes/new", methods=["GET", "POST"])
@login_required
def new_attribute(uuid):
    entity = Entities.query.filter(Entities.Id == uuid).first()

    if not entity:
        abort(404)

    form = AttributeViewModel()

    if request.method == "POST":
        if not form.validate():
            return render_template("attributes/create.html", form=form)
        else:
            attribute = form.domain()
            attribute.Entity = entity

            db.session.add(attribute)
            db.session.commit()
            return redirect(url_for("entity_info", uuid=uuid))

    return render_template("attributes/create.html", form=form)


@app.route("/attributes/<uuid>/update", methods=["GET", "POST"])
@login_required
def update_attribute(uuid):
    attribute = Attributes.query.filter(Attributes.Id == uuid).first()
    form = attribute.wtf()
    form.Entity.choices = [(str(entity.Id), f"{entity.Name} ({entity.Schema.Name})") for entity
                           in Entities.query.join(Schemas, Entities.SchemaIdFk == Schemas.Id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("attributes/update.html", form=form)
        attribute.map_from(form)
        db.session.commit()
        return redirect(url_for("entity_info", uuid=attribute.EntityIdFk))

    return render_template("attributes/update.html", form=form)


@app.route("/attributes/delete/<uuid>", methods=["POST"])
@login_required
def delete_attribute(uuid):
    attribute = Attributes.query.filter(Attributes.Id == uuid).first()
    if attribute:
        db.session.delete(attribute)
        db.session.commit()

    return redirect(url_for("entity_info", uuid=attribute.EntityIdFk))


@app.route("/dashboard")
@login_required
def dashboard():
    all_schemas = db.session.query(Schemas.Id, Schemas.Name).all()
    distinct_entities = db.session.query(Entities.Name).distinct().all()
    dashboardViewModel = DashboardViewModel()
    if len(all_schemas):
        dashboardViewModel.Schemas = [(str(schema.Id), schema.Name) for schema in all_schemas]
        dashboardViewModel.Schemas_distribution_data = schema_distribution_pie(all_schemas[0][0])

    if len(distinct_entities):
        dashboardViewModel.Entities = distinct_entities
        dashboardViewModel.Entities_attributes_population_data = entity_attributes_population_bar(
            distinct_entities[0][0])

    return render_template("dashboard/index.html", model=dashboardViewModel)


@app.route("/schema_distribution/<uuid>")
@login_required
def schema_distribution(uuid):
    return schema_distribution_pie(uuid)


@app.route("/entity_attributes_population/<name>")
@login_required
def entity_attributes_population(name):
    return entity_attributes_population_bar(name)


@app.route("/classification", methods=["POST"])
def classify():
    return jsonify(classification(json.loads(request.get_data())))


@app.route("/statistics")
@login_required
def statistics():
    if not current_user.IsAdmin:
        return abort(404)

    model = StatisticsViewModel(correlation())
    return render_template("statistics/index.html", model=model)


@app.route("/users")
@login_required
def users():
    if not current_user.IsAdmin:
        return abort(404)

    users = Users.query.filter(Users.Username != current_user.Username).order_by(Users.Username).all()

    return render_template("admin/users.html", users=users)


@app.route("/grant_admin/<username>", methods=["POST"])
def grant_admin(username):
    if not current_user.IsAdmin:
        return abort(404)

    user = Users.query.filter(Users.Username == username).first()

    if user and not user.IsAdmin:
        user.IsAdmin = True
        db.session.commit()

    return redirect(url_for("users"))


@app.route("/ungrant_admin/<username>", methods=["POST"])
def ungrant_admin(username):
    if not current_user.IsAdmin:
        return abort(404)

    user = Users.query.filter(Users.Username == username).first()

    if user and user.IsAdmin:
        user.IsAdmin = False
        db.session.commit()

    return redirect(url_for("users"))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
