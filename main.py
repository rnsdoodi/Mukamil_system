from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

# Flask App
app = Flask(__name__)


all_users = []
all_arrived = []

# Creating The SQLALCHEMY DataBase
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Bootstrap App
Bootstrap(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Creating Table in the DB to Add New Customer Request
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    nid_or_iqama = db.Column(db.Integer, nullable=False)
    contact_No = db.Column(db.String(250), nullable=False)
    visa = db.Column(db.Integer, nullable=False)
    visa_date = db.Column(db.Date, nullable=False)
    worker_name = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(250), nullable=False)
    agency = db.Column(db.String(250), nullable=False)
    selected_or_recommended = db.Column(db.String(250), nullable=False)
    musaned = db.Column(db.String(250), nullable=False)
    embassy_contract = db.Column(db.String(250), nullable=False)
    shipment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(1000), nullable=False)


# CREATE TABLE IN DB To save users login Data (Hashed & Salted)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

db.create_all()
# Add Customer Request Flask Form for (السلالم الدولية)
class AddUser(FlaskForm):

    name = StringField('Employer Name/اسم العميل ', validators=[DataRequired()])
    nid_or_iqama = IntegerField('ID or IQAMA / الهوية الوطنية أو الإقامة', validators=[DataRequired()])
    contact_No = StringField('Mobile No/رقم الجوال', validators=[DataRequired()])
    visa = IntegerField('Visa No./رقم التأشيرة', validators=[DataRequired()])
    visa_date = DateField('Visa Date/تاريخ التأشيرة', validators=[DataRequired()],format='%Y-%m-%d')
    worker_name = StringField('Worker Name/إسم العاملة', validators=[DataRequired()])
    type = SelectField('Position/المهنة', choices=["عاملة منزلية/DH", "عامل منزلي/HOUSE BOY", "ممرضة منزلية/PRIVATE nURSE", "مربية/NANNY", "سائق خاص/FAMILY DRIVER"],
                       validators=[DataRequired()])
    agency = SelectField('Agency/المكتب', choices=["Domec", "Myriad", "Reenkam", "TradeFast", "بايونير", "الشريف"],
                         validators=[DataRequired()])
    selected_or_recommended = SelectField('Selected or Recommended/معينة ام مختارة',
                                          choices=["معينة Recommended", "مختارة Selected"], validators=[DataRequired()])
    musaned = SelectField('Musaned Contract/عقد مساند', choices=["✔ نعم", " ❌ لا"], validators=[DataRequired()])
    embassy_contract = SelectField('Embassy Contract/عقد السفارة', choices=["✔ نعم", " ❌ لا"], validators=[DataRequired()])
    shipment_date = DateField(' Shipment Date/تاريخ الإرسالية', validators=[DataRequired()], format='%Y-%m-%d')
    status = StringField(' Status/الحالة')
    submit = SubmitField('Add إضافة')


# Edit Customer Request Flask Form for (السلالم الدولية)
class EditUser(FlaskForm):
    musaned = SelectField('Musaned Contract/عقد مساند', choices=["✔ نعم", " ❌ لا"])
    embassy_contract = SelectField('Embassy Contract/عقد السفارة', choices=["✔ نعم", " ❌ لا"])
    shipment_date = DateField(' Shipment Date/تاريخ الإرسالية', validators=[DataRequired()])
    status = StringField('Status/الحالة')
    submit = SubmitField('تعديل')

# Edit Worker Status Flask Form for (Domec)


class DomecEditUser(FlaskForm):
    status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Change')

#######################################################################################################################
                       # Authentication Part for (السلالم الدولية) :- #


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route('/salalim')
def sign():
    return render_template("main.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get('email')).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("تم التسجيل بنجاح, رجاءا قم بالعودة الى صفحة الدخول")
        return redirect(url_for("register"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('sign'))


#######################################################################################################################
                # Backend For (السلالم الدولية ) including the CRUD Operations form the DB #

@app.route("/")
def index():
    all_users = Users.query.all()
    return render_template("index.html", users=all_users)


@app.route("/index.html")
@login_required
def home():
    print(current_user.name)
    all_users = Users.query.all()
    return render_template("index.html", users=all_users, name=current_user.name, logged_in=True)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddUser()

    if form.validate_on_submit():
        new_user = Users(
            name=form.name.data,
            nid_or_iqama=form.nid_or_iqama.data,
            contact_No=form.contact_No.data,
            visa=form.visa.data,
            visa_date=form.visa_date.data,
            worker_name=form.worker_name.data,
            type=form.type.data,
            agency=form.agency.data,
            selected_or_recommended=form.selected_or_recommended.data,
            musaned=form.musaned.data,
            embassy_contract=form.embassy_contract.data,
            shipment_date=form.shipment_date.data,
            status=form.status.data
        )

        db.session.add(new_user)
        db.session.commit()
        all_users.append(new_user)
        flash("تمت الإضافة بنجاح ✔!!")
        return redirect(url_for('add'))
    return render_template("add.html", form=form)


@app.route("/list")
def users_list():
    added_users = Users.query.all()
    return render_template("list.html", users=added_users, name=current_user.name)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditUser()
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    if form.validate_on_submit():
        updated_user.musaned = form.musaned.data
        updated_user.embassy_contract = form.embassy_contract.data
        updated_user.shipment_date = form.shipment_date.data
        updated_user.status = form.status.data

        db.session.commit()
        flash("تم تعديل بيانات العميل بنجاح✔")
        return redirect(url_for('edit'))
    return render_template("edit.html", form=form, user=updated_user)


@app.route("/delete")
def delete():
    user_id = request.args.get("id")
    user_to_delete = Users.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("تم حذف بيانات العميل بنجاح✔")
    return redirect(url_for('users_list'))


@app.route("/tables")
def tables():
    added_users = Users.query.all()
    return render_template("tables.html", users=added_users, name=current_user.name, logged_in=True)


@app.route("/conditions")
def conditions():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


#######################################################################################################################
                                # Authentication Part for (Domec) :- #


@app.route('/domec')
def domec_sign():
    return render_template("domec_main.html")


@app.route('/domec_register', methods=["GET", "POST"])
def domec_register():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get('email')).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('domec_login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("تم التسجيل بنجاح, فضلاً قم بالعودة الى صفحة الدخول")
        return redirect(url_for("domec_register"))

    return render_template("domec_register.html", logged_in=current_user.is_authenticated)


@app.route('/domec_login', methods=["GET", "POST"])
def domec_login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('domec_login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('domec_login'))
        else:
            login_user(user)
            return redirect(url_for('domec_home'))

    return render_template("domec_login.html", logged_in=current_user.is_authenticated)


@app.route('/domec_logout')
def domec_logout():
    logout_user()
    return redirect(url_for('domec_sign'))


#######################################################################################################################
                   # Backend For (DOMEC) including the CRUD Operations form the DB #


@app.route("/Domec_login")
def domec_index():
    all_users = Users.query.all()
    return render_template("domec_index.html", users=all_users)


@app.route("/domec-index.html")
@login_required
def domec_home():
    print(current_user.name)
    all_users = Users.query.all()
    return render_template("domec_index.html", users=all_users, name=current_user.name, logged_in=True)

# @app.route("/add", methods=["GET", "POST"])
# def add():
#     form = AddUser()
#
#     if form.validate_on_submit():
#         new_user = Users(
#             name=form.name.data,
#             nid_or_iqama=form.nid_or_iqama.data,
#             contact_No=form.contact_No.data,
#             visa=form.visa.data,
#             visa_date=form.visa_date.data,
#             worker_name=form.worker_name.data,
#             type=form.type.data,
#             agency=form.agency.data,
#             selected_or_recommended=form.selected_or_recommended.data,
#             musaned=form.musaned.data,
#             embassy_contract=form.embassy_contract.data,
#             shipment_date=form.shipment_date.data,
#             status=form.status.data
#         )
#
#         db.session.add(new_user)
#         db.session.commit()
#         all_users.append(new_user)
#         flash("تمت الإضافة بنجاح ✔!!")
#         return redirect(url_for('add'))
#     return render_template("add.html", form=form)


@app.route("/domec_list")
def domec_users_list():
    added_users = Users.query.all()
    return render_template("domec_list.html", users=added_users, name=current_user.name)


@app.route("/domec_edit", methods=["GET", "POST"])
def domec_edit():
    form = DomecEditUser()
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    if form.validate_on_submit():
        updated_user.status = form.status.data
        db.session.commit()
        flash("Status successfully Changed ✔")
        return redirect(url_for('domec_edit'))
    return render_template("domec_edit.html", form=form, user=updated_user)


@app.route("/domec_delete")
def domec_delete():
    user_id = request.args.get("id")
    user_to_delete = Users.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("Customer Request Deleted Successfully ✔")
    return redirect(url_for('domec_users_list.html'))


@app.route("/domec_tables")
def domec_tables():
    added_users = Users.query.all()
    return render_template("domec_tables.html", users=added_users, name=current_user.name, logged_in=True)

########################################################################################################################


if __name__ == "__main__":
    app.run(debug=True)
