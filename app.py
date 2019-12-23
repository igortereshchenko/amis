from flask import Flask, request, render_template, redirect, url_for
from domain.models import db, Users, Events, Options, Clothes, Vendors,Favors
from domain.credentials import *
from views.users import UsersViewModel
from views.events import EventsViewModel
from views.options import OptionsViewModel
from views.clothes import ClothesViewModel
from views.vendors import VendorsViewModel
from views.favors import FavorsViewModel
from views.auth import LoginViewModel
from services.visualization import visualization_data
from sqlalchemy import desc
import os
from nn import *
from flask_login import login_user, login_required, current_user, logout_user, LoginManager

app = Flask(__name__)
app.secret_key = 'development key'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)




@app.route("/")
def root():
    db.create_all()
    return render_template("layout.html")

@app.route('/map')
def map():
    db.create_all()
    user_1=Users(Login='Kolobaieva',Password='1111',Email='dddd@gmail.com',Lastname='Kolobaieva',Firstname='Katia',Age='20',Eyes='blue',hair='brown', height='160')
    event_1=Events(event_name='birthday',user_idIDFK='1')
    option_1=Options(place='cafe',season='summer',temperature='20',event_idIDFK='1')
    clothe_1=Clothes(style_name='romantic',outwear='t-shirt',lowerwear='jeans',shoes='35',option_idIDFK='1')
    vendor_1=Vendors(vendor_name='Katia',vendor_address='kyiv', balance='2000',vendor_country='UK',clothe_idIdFk='1')
    db.session.add_all([user_1,event_1,option_1,clothe_1,vendor_1])
    db.session.commit()
    return render_template("layout.html")

@app.route('/get')
def get():
    users=Users.query.all()
    events=Events.query.all()
    options=Options.query.all()
    clothes=Clothes.query.all()
    vendors=Vendors.query.all()
    return render_template("layout.html",users=users,events=events,options=options,clothes=clothes,vendors=vendors)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginViewModel()
    if request.method == 'POST':
        if not form.validate():
            render_template("authentication/index.html", form=form)
        else:
            Login = form.Login.data
            Password = form.Password.data
            log = db.session.query(Users).filter(Users.Login == Login).filter(Users.Password == Password).all()
            if log:

                if Login == 'Kolobayeva':
                    return redirect(url_for('users'))
            return redirect(url_for('new_user', user=Login))
        return render_template("authentication/index.html", form=form, message='not found')

    return render_template("authentication/index.html", form=form)







@app.route("/users")
def users():
    all_users = Users.query.all()
    return render_template("users/index.html", users=all_users)


@app.route("/users/new", methods=["GET", "POST"])
def new_user():
    form = UsersViewModel()

    if request.method == "POST":
        if not form.validate():
            return render_template("users/create.html", form=form)
        else:
            user = form.domain()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("users"))

    return render_template("users/create.html", form=form)


@app.route("/users/delete/<uuid>", methods=["POST"])
def delete_user(uuid):
    user = Users.query.filter(Users.user_id == uuid).first()
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("users"))


@app.route("/users/<uuid>", methods=["GET", "POST"])
def update_user(uuid):
    user = Users.query.filter(Users.user_id == uuid).first()
    form = user.wtf()

    if request.method == "POST":
        if not form.validate():
            return render_template("users/update.html", form=form)

        user.map_from(form)
        db.session.commit()
        return redirect(url_for("users"))

    return render_template("users/update.html", form=form)

@app.route("/events")
def events():
    all_events = Events.query.join(Users).order_by(desc(Events.CreatedOn)).all()
    return render_template("events/index.html", events=all_events)


@app.route("/events/new", methods=["GET", "POST"])
def new_event():
    form = EventsViewModel()
    form.User.choices = [(str(user.user_id), user.Login) for user in Users.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("events/create.html", form=form)
        else:
            user = form.domain()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("events"))

    return render_template("events/create.html", form=form)


@app.route("/events/delete/<uuid>", methods=["POST"])
def delete_event(uuid):
    event = Events.query.filter(Events.event_id == uuid).first()
    if event:
        db.session.delete(event)
        db.session.commit()

    return redirect(url_for("events"))


@app.route("/events/<uuid>", methods=["GET", "POST"])
def update_event(uuid):
    event = Events.query.filter(Events.event_id == uuid).first()
    form = event.wtf()
    form.User.choices = [(str(user.user_id), user.Login) for user in Users.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("events/update.html", form=form)
        event.map_from(form)
        db.session.commit()
        return redirect(url_for("events"))

    return render_template("events/update.html", form=form)

@app.route("/options")
def options():
    all_options = Options.query.join(Events).order_by(desc(Options.CreatedOn)).all()
    return render_template("options/index.html", options=all_options)


@app.route("/options/new", methods=["GET", "POST"])
def new_option():
    form = OptionsViewModel()
    form.Event.choices = [(str(event.event_id), event.Event_name) for event in Events.query.join(Users, Events.user_idIdFk == Users.user_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("options/create.html", form=form)
        else:
            user = form.domain()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("options"))

    return render_template("options/create.html", form=form)


@app.route("/options/<uuid>", methods=["GET", "POST"])
def update_option(uuid):
    option = Options.query.filter(Options.option_id == uuid).first()
    form = option.wtf()
    form.Event.choices = [(str(event.event_id), event.Event_name) for event in
                          Events.query.join(Users, Events.user_idIdFk == Users.user_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("options/update.html", form=form)
        option.map_from(form)
        db.session.commit()
        return redirect(url_for("options"))

    return render_template("options/update.html", form=form)


@app.route("/options/delete/<uuid>", methods=["POST"])
def delete_option(uuid):
    option = Options.query.filter(Options.option_id == uuid).first()
    if option:
        db.session.delete(option)
        db.session.commit()

    return redirect(url_for("options"))

@app.route("/clothes")
def clothes():
    all_clothes = Clothes.query.join(Options).all()
    return render_template("clothes/index.html", clothes=all_clothes)


@app.route("/clothes/new", methods=["GET", "POST"])
def new_clothe():
    form = ClothesViewModel()
    form.Option.choices = [(str(option.option_id), option.Place) for option
                           in Options.query.join(Events, Options.event_idIdFk == Events.event_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("clothes/create.html", form=form)
        else:
            event = form.domain()
            db.session.add(event)
            db.session.commit()
            return redirect(url_for("clothes"))

    return render_template("clothes/create.html", form=form)


@app.route("/clothes/<uuid>", methods=["GET", "POST"])
def update_clothe(uuid):
    clothe = Clothes.query.filter(Clothes.clothe_id == uuid).first()
    form = clothe.wtf()
    form.Option.choices = [(str(option.option_id), option.Place) for option
                           in Options.query.join(Events, Options.event_idIdFk == Events.event_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("clothes/update.html", form=form)
        clothe.map_from(form)
        db.session.commit()
        return redirect(url_for("clothes"))

    return render_template("clothes/update.html", form=form)


@app.route("/clothes/delete/<uuid>", methods=["POST"])
def delete_clothe(uuid):
    clothe = Clothes.query.filter(Clothes.clothe_id == uuid).first()
    if clothe:
        db.session.delete(clothe)
        db.session.commit()

    return redirect(url_for("clothes"))



@app.route("/vendors")
def vendors():
    all_vendors = Vendors.query.join(Clothes).all()
    return render_template("vendors/index.html", vendors=all_vendors)

@app.route("/vendors/new", methods=["GET", "POST"])
def new_vendor():
    form = VendorsViewModel()
    form.Clothe.choices = [(str(clothe.clothe_id), clothe.Outwear) for clothe
                           in Clothes.query.join(Options, Clothes.option_idIdFk == Options.option_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("vendors/create.html", form=form)
        else:
            option = form.domain()
            db.session.add(option)
            db.session.commit()
            return redirect(url_for("vendors"))

    return render_template("vendors/create.html", form=form)


@app.route("/vendors/<uuid>", methods=["GET", "POST"])
def update_vendor(uuid):
    vendor = Vendors.query.filter(Vendors.vendor_id == uuid).first()
    form = vendor.wtf()
    form.Clothe.choices = [(str(clothe.clothe_id), clothe.Outwear) for clothe
                           in Clothes.query.join(Options, Clothes.option_idIdFk == Options.option_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("vendors/update.html", form=form)
        vendor.map_from(form)
        db.session.commit()
        return redirect(url_for("vendors"))

    return render_template("vendors/update.html", form=form)


@app.route("/vendors/delete/<uuid>", methods=["POST"])
def delete_vendor(uuid):
    vendor = Vendors.query.filter(Vendors.vendor_id == uuid).first()
    if vendor:
        db.session.delete(vendor)
        db.session.commit()

    return redirect(url_for("vendors"))

@app.route("/favors")
def favors():
    all_favors = Favors.query.join(Clothes).join(Vendors).all()
    return render_template("favors/index.html", favors=all_favors)

@app.route("/favors/new", methods=["GET", "POST"])
def new_favor():
    form = FavorsViewModel()
    form.Vendor.choices = [
        (str(vendor.vendor_id), vendor.vendor_name) for vendor in
        Vendors.query.all()]

    form.Clothe.choices = [(str(clothe.clothe_id), clothe.Outwear) for clothe in
                             Clothes.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("questionnaires/create.html", form=form)
        else:
            favor = form.domain()
            db.session.add(favor)
            db.session.commit()
            return redirect(url_for("favors"))

    return render_template("favors/create.html", form=form)


@app.route("/favors/delete/<uuid>", methods=["POST"])
def delete_favor(uuid):
    favor = Favors.query.filter(Favors.favors_id == uuid).first()
    if favor:
        db.session.delete(favor)
        db.session.commit()

    return redirect(url_for("favors"))


@app.route("/favors/<uuid>", methods=["GET", "POST"])
def update_favor(uuid):
    favor = Favors.query.filter(Favors.favors_id == uuid).first()
    form = favor.wtf()
    form.Vendor.choices = [
        (str(vendor.vendor_id), vendor.vendor_name) for vendor in
        Vendors.query.all()]

    form.Clothe.choices = [(str(clothe.clothe_id), clothe.Outwear) for clothe in
                             Clothes.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("favors/update.html", form=form)

        favor.map_from(form)
        db.session.commit()
        return redirect(url_for("favors"))

    return render_template("favors/update.html", form=form)

@app.route("/bar", methods=["GET"])
def visualization():
    data = visualization_data()
    return render_template("dashboard/index.html", clothe_vendors_bar=data)



if __name__ == "__main__":
    app.run(debug=True)
