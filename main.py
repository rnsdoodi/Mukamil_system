from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, length
from wtforms.fields.html5 import DateField
import os

# Flask App
app = Flask(__name__)

# app._static_folder = ''
# static = safe_join(os.path.dirname(__file__), 'static')


all_users = []
all_arrived = []
all_skills = []
all_transfers = []

# Creating The SQLALCHEMY DataBase
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "ANY SECRET KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///users.db")
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
    nid_or_iqama = db.Column(db.String, nullable=False)
    contact_No = db.Column(db.String(250), nullable=False)
    visa = db.Column(db.String, nullable=False)
    visa_date = db.Column(db.Date, nullable=False)
    worker_name = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(250), nullable=False)
    agency = db.Column(db.String(250), nullable=False)
    selected_or_recommended = db.Column(db.String(250), nullable=False)
    musaned = db.Column(db.String(250), nullable=False)
    embassy_contract = db.Column(db.String(250), nullable=False)
    shipment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(1000), nullable=False)


# Creating Table in the DB to Add New skilled Request
class Skilled(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False)
    company_visa = db.Column(db.String, nullable=False)
    cr = db.Column(db.String, nullable=False)
    contact_No = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)
    mp_request = db.Column(db.String(250), nullable=False)
    quantity = db.Column(db.String(250), nullable=False)
    selected_or_recommended = db.Column(db.String(250), nullable=False)
    agency = db.Column(db.String(250), nullable=False)
    jo_status = db.Column(db.String(250), nullable=False)
    shipment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(1000), nullable=False)


class Transfer(db.Model):
    __tablename__ = "transfer"
    id = db.Column(db.Integer, primary_key=True)
    first_employer_name = db.Column(db.String(250), nullable=False)
    first_contact_no = db.Column(db.String(250), nullable=False)
    worker_name = db.Column(db.String(250), nullable=False)
    worker_contact_no = db.Column(db.String(250), nullable=False)
    second_employer_name = db.Column(db.String(250), nullable=False)
    second_contact_no = db.Column(db.String(250), nullable=False)
    iqama = db.Column(db.String(250), nullable=False)
    agency = db.Column(db.String(250), nullable=False)
    request_status = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(250), nullable=False)


# CREATE TABLE IN DB To save users login Data (Hashed & Salted)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


db.create_all()


# Add Customer Request Flask Form for (السلالم الدولية)
class AddUser(FlaskForm):
    name = StringField('اسم العميل ', validators=[DataRequired(), length(max=100)])
    nid_or_iqama = StringField(' الهوية الوطنية أو الإقامة', validators=[DataRequired(), length(max=10)],
                               description="ادخل رقم هوية صالح مكون من 10 ارقام")
    contact_No = StringField('رقم الجوال', validators=[DataRequired()],
                             description='05xxxxxxxx : مثال')
    visa = StringField('رقم التأشيرة', validators=[DataRequired(), length(max=10)],
                       description="ادخل رقم تأشيرة صالح مكون من 10 ارقام")
    visa_date = DateField('تاريخ الطلب', validators=[DataRequired()], format='%Y-%m-%d')
    worker_name = StringField('إسم العاملة', validators=[DataRequired(), length(max=150)],
                              description='كما هو مدون في جواز السفر')
    type = SelectField('المهنة',
                       choices=["عاملة منزلية/DH", "عامل منزلي/HOUSE BOY", "ممرضة منزلية/PRIVATE NURSE", "مربية/NANNY",
                                "سائق خاص/FAMILY DRIVER"])
    agency = SelectField('المكتب', choices=["Domec", "Myriad", "Reenkam", "TradeFast", "بايونير", "الشريف", "Imran "
                                                                                                            "International"])
    selected_or_recommended = SelectField('معينة ام مختارة',
                                          choices=[" Recommended", " Selected"])
    musaned = SelectField('عقد مساند', choices=["  Yes", "   No"])
    embassy_contract = SelectField('عقد السفارة', choices=["  Yes", "  No"])
    shipment_date = DateField(' تاريخ الإرسالية', format='%Y-%m-%d')
    status = StringField(' الحالة', validators=[length(max=200)])
    submit = SubmitField('Add إضافة')


# Edit Customer Request Flask Form for (السلالم الدولية)
class EditUser(FlaskForm):
    musaned = SelectField('عقد مساند', choices=["  Yes", "   No"])
    embassy_contract = SelectField('عقد السفارة', choices=[" Yes", "   No"])
    shipment_date = DateField(' تاريخ الإرسالية', format='%Y-%m-%d')
    status = StringField('الحالة', validators=[length(max=200)])
    submit = SubmitField('تــعـديــل')


# Add new skills Request Flask Form for (السلالم الدولية)


class AddSkills(FlaskForm):
    company_name = StringField('اسم المؤسسة  ', validators=[DataRequired(), length(max=100)])
    company_visa = StringField('رقم التأشيرة', validators=[DataRequired(), length(max=10)],
                               description="ادخل رقم تأشيرة صالح مكون من 10 ارقام")
    cr = StringField(' السجل التجاري', validators=[DataRequired(), length(max=10)],
                     description="ادخل الرقم الموحد للمنشأة يبدا ب 70")

    contact_No = StringField('رقم الجوال', validators=[DataRequired()],
                             description='05xxxxxxxx : مثال')

    country = SelectField('الدولة', choices=[" Philippines", "Thailand", "India", "Pakistan", "Nepal", "Tunisia",
                                             "Morocco", "Egypt", "Sudan"])
    mp_request = StringField('المهنة', validators=[DataRequired(), length(max=150)],
                             description='كما هو مدون في التأشيرة ')
    quantity = StringField('العدد', validators=[DataRequired(), length(max=150)])
    selected_or_recommended = SelectField('معينة ام مختارة',
                                          choices=[" Recommended", " Selected"])
    agency = SelectField('المكتب', choices=["Domec", "Myriad", "Reenkam", "TradeFast", "بايونير", "الشريف",
                                            "Imran International","World Vision Int."])
    jo_status = SelectField('حالة الجوب اوردر', choices=["For POLO Verification", "Verified From POLO and sent Via DHL",
                                                         "For POEA Approval", "POEA Approved",
                                                         "INDIAN IMMIGRATION APPROVED"])
    shipment_date = DateField(' تاريخ الإرسالية', format='%Y-%m-%d')
    status = StringField(' حالة الطلب', validators=[DataRequired(), length(max=1000)])
    submit = SubmitField('Add إضافة')


# Edit new skills Request Flask Form for (السلالم الدولية)

class EditSkills(FlaskForm):
    jo_status = SelectField('حالة الجوب اوردر', choices=["For POLO Verification", "Verified From POLO and sent Via DHL",
                                                         "For POEA Approval", "POEA Approved"])
    shipment_date = DateField(' تاريخ الإرسالية', format='%Y-%m-%d')
    status = StringField(' حالة الطلب', validators=[length(max=1000)])
    submit = SubmitField('تــعـديــل')


# Add new Transfer Request Flask Form for (السلالم الدولية)

class AddTransfer(FlaskForm):
    first_employer_name = StringField('اسم الكفيل الأول ', validators=[DataRequired(), length(max=100)])
    first_contact_no = StringField('رقم جوال الكفيل الأول', validators=[DataRequired(), length(max=100)],
                                   description="ادخل رقم جوال صالح مكون من 10 ارقام")
    worker_name = StringField('  اسم العاملة ', validators=[DataRequired(), length(max=100)],
                              description="كما هو مدون في جواز السفر")
    worker_contact_no = StringField('رقم جوال العاملة', description='إن وجد')
    second_employer_name = StringField('اسم الكفيل الثاني', validators=[DataRequired(), length(max=100)])
    second_contact_no = StringField('رقم جوال الكفيل الثاني', validators=[DataRequired(), length(max=150)],
                                    description='ادخل رقم جوال صالح مكون من 10 ارقام ')
    iqama = SelectField(' الإقامة', choices=["نعم", "لا"])
    agency = SelectField('المكتب', choices=["Domec", "Myriad", "Jinhel", "Reenkam", "الصالح", "الشريف "])
    request_status = SelectField('حالة الطلب', choices=["العاملة في فترة التجربة",
                                                        "أكملت العاملة فترة التجربة وجاري إنهاء أجراءات نقل الخدمات",
                                                        "في انتظار سداد رسوم الإقامة / نقل الكفالة",
                                                        "تم نقل الخدمات",
                                                        "العاملة رفضت نقل الخدمات وتراجعت"])
    status = StringField('  ملاحظات ', validators=[DataRequired(), length(max=300)])
    submit = SubmitField('إضــافـة الطلــب')


# Edit new Transfer Request Flask Form for (السلالم الدولية)
class EditTransfer(FlaskForm):
    iqama = SelectField(' الإقامة', choices=["نعم", "لا"])
    reqeust_status = StringField('حالة الطلب', validators=[DataRequired(), length(max=300)])
    status = StringField('  ملاحظات ', validators=[DataRequired(), length(max=300)])
    submit = SubmitField('تــعـديــل')


#######################################################################################################################


# Add Customer Request Flask Form for (Domec)
class AddCustomer(FlaskForm):
    name = StringField('Employer Name ', validators=[DataRequired(), length(max=100)])
    nid_or_iqama = StringField('ID or IQAMA ', validators=[DataRequired(), length(max=10)],
                               description="Pleases insert correct ID No.")
    contact_No = StringField('Mobile No.', validators=[DataRequired()],
                             description='example : 05xxxxxxxx')
    visa = StringField('Visa No.', validators=[DataRequired(), length(max=10)],
                       description="Please insert correct 10 digits visa No.")
    visa_date = DateField('Request Date', validators=[DataRequired()], format='%Y-%m-%d')
    worker_name = StringField('Worker Name', validators=[DataRequired(), length(max=150)],
                              description='As per the Passport')
    type = SelectField('Position',
                       choices=["DH", "HOUSE BOY", "PRIVATE NURSE", "NANNY",
                                "FAMILY DRIVER"])
    agency = SelectField('Agency', choices=["Domec", "Myriad", "Reenkam", "TradeFast", "بايونير", "الشريف"])
    selected_or_recommended = SelectField('Selected or Recommended',
                                          choices=[" Recommended", " Selected"])
    musaned = SelectField('Musaned Contract', choices=["  Yes", "   No"])
    embassy_contract = SelectField('Original Contract', choices=["  Yes", "  No"])
    shipment_date = DateField(' Shipment Date', format='%Y-%m-%d')
    status = StringField(' Status', validators=[length(max=200)])
    submit = SubmitField('Add')


# Edit Worker Status Flask Form for (Domec)

class DomecEditUser(FlaskForm):
    status = StringField('Status', validators=[DataRequired(), length(max=200)])
    submit = SubmitField('Change')


# Add new skills Request Flask Form for (Domec)

class DomecAddSkills(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), length(max=100)])
    company_visa = StringField('Visa No. ', validators=[DataRequired(), length(max=10)],
                               description="Please insert 10 digits Valid visa No.")
    cr = StringField('Commercial Registration ', validators=[DataRequired(), length(max=10)],
                     description="Please Insert valid Unified National Number starting by 70")

    contact_No = StringField('Mobile No.', validators=[DataRequired()],
                             description=' Example : 05xxxxxxxx ')

    country = StringField('Country', validators=[DataRequired()])
    mp_request = StringField('Position', validators=[DataRequired(), length(max=150)],
                             description='As Per the Visa ')
    quantity = StringField('Quantity', validators=[DataRequired(), length(max=150)])
    selected_or_recommended = SelectField('Selected or Recommended ',
                                          choices=[" Recommended", " Selected"])
    agency = SelectField('Agency', choices=["Domec", "Myriad", "Reenkam", "TradeFast", "Pioneer", "Alshareef"])
    jo_status = SelectField('Job Order Status', choices=["For POLO Verification", "Verified From POLO and sent Via DHL",
                                                         "For POEA Approval", "POEA Approved"])
    shipment_date = DateField(' Shipment Date', format='%Y-%m-%d')
    status = StringField(' Status', validators=[length(max=500)])
    submit = SubmitField('Add')


# Edit new skills Request Flask Form for (Domec)

class DomecEditSkills(FlaskForm):
    jo_status = SelectField('Job Order Status', choices=["For POLO Verification", "Verified From POLO and sent Via DHL",
                                                         "For POEA Approval", "POEA Approved"])
    status = StringField(' Status', validators=[length(max=1000)])
    submit = SubmitField('Update')


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


@app.route("/skills_index")
@login_required
def skills():
    print(current_user.name)
    all_skills = Skilled.query.all()
    return render_template("skills_index.html", skills=all_skills, name=current_user.name, logged_in=True)


@app.route("/transfer_index")
@login_required
def transfer():
    print(current_user.name)
    all_transfers = Transfer.query.all()
    return render_template("transfer_index.html", transfers=all_transfers, name=current_user.name, logged_in=True)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddUser()

    if form.validate_on_submit():
        new_customer = Users(
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

        db.session.add(new_customer)
        db.session.commit()
        all_users.append(new_customer)
        flash("تمت اضافة طلب العمالة المنزلية بنجاح ✔!!")
        return redirect(url_for('add'))
    return render_template("add.html", form=form)


@app.route("/skills_add", methods=["GET", "POST"])
def skills_add():
    form = AddSkills()
    if form.validate_on_submit():
        new_skills = Skilled(
            company_name=form.company_name.data,
            company_visa=form.company_visa.data,
            cr=form.cr.data,
            contact_No=form.contact_No.data,
            country=form.country.data,
            mp_request=form.mp_request.data,
            quantity=form.quantity.data,
            selected_or_recommended=form.selected_or_recommended.data,
            agency=form.agency.data,
            jo_status=form.jo_status.data,
            shipment_date=form.shipment_date.data,
            status=form.status.data
        )

        db.session.add(new_skills)
        db.session.commit()
        all_skills.append(new_skills)
        flash("تمت اضافة طلب العمالة المهنية بنجاح ✔!!")
        return redirect(url_for('skills_add'))
    return render_template("skills_add.html", form=form)


@app.route("/transfer_add", methods=["GET", "POST"])
def add_transfer():
    form = AddTransfer()
    if form.validate_on_submit():
        new_transfer = Transfer(
            first_employer_name=form.first_employer_name.data,
            first_contact_no=form.first_contact_no.data,
            worker_name=form.worker_name.data,
            worker_contact_no=form.worker_contact_no.data,
            second_employer_name=form.second_employer_name.data,
            second_contact_no=form.second_contact_no.data,
            iqama=form.iqama.data,
            agency=form.agency.data,
            request_status=form.request_status.data,
            status=form.status.data,
        )
        db.session.add(new_transfer)
        db.session.commit()
        all_skills.append(new_transfer)
        flash("تم اضافة طلب نقل الخدمة بنجاح ✔!!")
        return redirect(url_for('transfer_add'))
    return render_template("transfer_add.html", form=form)


@app.route("/list")
def users_list():
    added_users = Users.query.all()
    return render_template("list.html", users=added_users, name=current_user.name)


@app.route("/skills_list")
def skills_list():
    added_skills = Skilled.query.all()
    return render_template("skills_list.html", skills=added_skills, name=current_user.name)


@app.route("/transfer_list")
def transfer_list():
    added_transfers = Transfer.query.all()
    return render_template("transfer_list.html", transfers=added_transfers, name=current_user.name)


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
        flash("تم تعديل بيانات طلب العمالة المنزلية بنجاح✔")
        return redirect(url_for('edit'))
    return render_template("edit.html", form=form, user=updated_user)


@app.route("/skills_edit", methods=["GET", "POST"])
def skills_edit():
    form = EditSkills()
    skills_id = request.args.get("id")
    updated_skills = Skilled.query.get(skills_id)
    if form.validate_on_submit():
        updated_skills.jo_status = form.jo_status.data
        updated_skills.shipment_date = form.shipment_date.data
        updated_skills.status = form.status.data

        db.session.commit()
        flash("تم تعديل حالة طلب العمالة المهنية بنجاح✔")
        return redirect(url_for('skills_edit'))
    return render_template("skills_edit.html", form=form, skill=updated_skills)


@app.route("/transfer_edit", methods=["GET", "POST"])
def transfer_edit():
    form = EditTransfer()
    transfer_id = request.args.get("id")
    updated_transfers = Transfer.query.get(transfer_id)
    if form.validate_on_submit():
        updated_transfers.iqama = form.iqama.data
        updated_transfers.request_status = form.reqeust_status.data
        updated_transfers.status = form.status.data

        db.session.commit()
        flash("تم تعديل حالة طلب نقل الخدمة بنجاح✔")
        return redirect(url_for('transfer_edit'))
    return render_template("transfers_edit.html", form=form, transfer=updated_transfers)


@app.route("/delete")
def delete():
    user_id = request.args.get("id")
    user_to_delete = Users.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("تم حذف بيانات العميل بنجاح✔")
    return redirect(url_for('users_list'))


@app.route("/skills_delete")
def skills_delete():
    skills_id = request.args.get("id")
    skills_to_delete = Skilled.query.get(skills_id)
    db.session.delete(skills_to_delete)
    db.session.commit()
    flash("تم حذف بيانات طلب العمالة المهنية بنجاح✔")
    return redirect(url_for('skills_list'))


@app.route("/transfer_delete")
def transfer_delete():
    transfer_id = request.args.get("id")
    transfers_to_delete = Transfer.query.get(transfer_id)
    db.session.delete(transfers_to_delete)
    db.session.commit()
    flash("تم حذف بيانات طلب نقل الخدمة بنجاح✔")
    return redirect(url_for('transfer_list'))


@app.route("/tables")
def tables():
    added_users = Users.query.all()
    return render_template("tables.html", users=added_users, name=current_user.name, logged_in=True)


@app.route("/skills_tables")
def skills_tables():
    added_skills = Skilled.query.all()
    return render_template("skills_tables.html", skills=added_skills, name=current_user.name, logged_in=True)


@app.route("/transfer_tables")
def transfers_tables():
    added_transfers = Transfer.query.all()
    return render_template("transfer_tables.html", transfers=added_transfers, name=current_user.name, logged_in=True)


@app.route("/conditions")
def conditions():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/download")
def download():
    return send_from_directory('static', filename="files/user's manual.pdf")


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


@app.route("/dom_skills_index.html")
@login_required
def dom_skills():
    print(current_user.name)
    all_skills = Skilled.query.all()
    return render_template("dom_skills_index.html", skills=all_skills, name=current_user.name, logged_in=True)


@app.route("/domec_add", methods=["GET", "POST"])
def domec_add():
    form = AddCustomer()

    if form.validate_on_submit():
        new_request = Users(
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

        db.session.add(new_request)
        db.session.commit()
        all_users.append(new_request)
        flash("successfully Added New Customer ✔!!")
        return redirect(url_for('domec_add'))
    return render_template("domec_add.html", form=form)


@app.route("/domec_add_skills", methods=["GET", "POST"])
def domec_add_skills():
    form = DomecAddSkills()

    if form.validate_on_submit():
        new_skills = Skilled(
            company_name=form.company_name.data,
            company_visa=form.company_visa.data,
            cr=form.cr.data,
            contact_No=form.contact_No.data,
            country=form.country.data,
            mp_request=form.mp_request.data,
            quantity=form.quantity.data,
            selected_or_recommended=form.selected_or_recommended.data,
            agency=form.agency.data,
            jo_status=form.jo_status.data,
            shipment_date=form.shipment_date.data,
            status=form.status.data
        )

        db.session.add(new_skills)
        db.session.commit()
        all_users.append(new_skills)
        flash("successfully Added New Skills Request ✔!!")
        return redirect(url_for('domec_add_skills'))
    return render_template("dom_skills_add.html", form=form)


@app.route("/domec_list")
def domec_users_list():
    added_users = Users.query.all()
    return render_template("domec_list.html", users=added_users, name=current_user.name)


@app.route("/domec_skills_list")
def domec_skills_list():
    added_skills = Skilled.query.all()
    return render_template("dom_skills_list.html", skills=added_skills, name=current_user.name)


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


@app.route("/domec_edit_skills", methods=["GET", "POST"])
def domec_edit_skills():
    form = DomecEditSkills()
    skills_id = request.args.get("id")
    updated_skills = Skilled.query.get(skills_id)
    if form.validate_on_submit():
        updated_skills.jo_status = form.jo_status.data
        updated_skills.status = form.status.data
        db.session.commit()
        flash("Status successfully Changed ✔")
        return redirect(url_for('domec_edit_skills'))
    return render_template("dom_skills_edit.html", form=form, skill=updated_skills)


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


@app.route("/domec_skills_tables")
def domec_skills_tables():
    added_skills = Skilled.query.all()
    return render_template("dom_skills_tables.html", skills=added_skills, name=current_user.name, logged_in=True)


########################################################################################################################


if __name__ == "__main__":
    app.run(debug=True)
