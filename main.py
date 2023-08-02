from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, length
from wtforms.fields.html5 import DateField
import os

# Flask App
app = Flask(__name__)

all_users = []
all_arrived = []
all_skills = []
all_transfers = []
all_nominates = []
all_complaints = []
all_procedures = []

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
    nid_or_iqama = db.Column(db.BIGINT, nullable=False)
    contact_No = db.Column(db.BIGINT, nullable=False)
    visa = db.Column(db.BIGINT, nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    worker_name = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(250), nullable=False)
    agency = db.Column(db.String(250), nullable=False)
    selected_or_recommended = db.Column(db.String(250), nullable=False)
    musaned = db.Column(db.String(250), nullable=False)
    embassy_contract = db.Column(db.String(250), nullable=False)
    shipment_date = db.Column(db.Date, nullable=False)
    medical = db.Column(db.String(500), nullable=True)
    mmr_vaccine = db.Column(db.String(500), nullable=True)
    owwa = db.Column(db.String(500), nullable=True)
    tesda = db.Column(db.String(500), nullable=True)
    biometric = db.Column(db.String(500), nullable=True)
    stamping = db.Column(db.String(500), nullable=True)
    oec = db.Column(db.String(500), nullable=True)
    ticket = db.Column(db.String(500), nullable=True)
    deployment_date = db.Column(db.String(500), nullable=True)  # Salalim Remarks
    status = db.Column(db.String(1000), nullable=True)


# Creating Table in the DB to Add New skilled Request
class Skilled(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False)
    company_visa = db.Column(db.BIGINT, nullable=False)
    cr = db.Column(db.BIGINT, nullable=False)
    contact_No = db.Column(db.BIGINT, nullable=False)
    country = db.Column(db.String(250), nullable=False)
    mp_request = db.Column(db.String(250), nullable=False)
    quantity = db.Column(db.String(250), nullable=False)
    selected_or_recommended = db.Column(db.String(250), nullable=False)
    agency = db.Column(db.String(250), nullable=False)
    jo_status = db.Column(db.String(250), nullable=False)
    shipment_date = db.Column(db.String(250), nullable=True) # salalim remarks
    status = db.Column(db.String(1000), nullable=True)


class Transfer(db.Model):
    __tablename__ = "transfer1"
    id = db.Column(db.Integer, primary_key=True)
    first_employer_name = db.Column(db.String(250), nullable=False)
    first_contact_no = db.Column(db.BIGINT, nullable=False)
    worker_name = db.Column(db.String(250), nullable=False)
    worker_contact_no = db.Column(db.BIGINT, nullable=False)
    second_employer_name = db.Column(db.String(250), nullable=False)
    second_contact_no = db.Column(db.BIGINT, nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    iqama = db.Column(db.String(250), nullable=False)
    agency = db.Column(db.String(250), nullable=False)
    request_status = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(1000), nullable=False)


# Creating Table in the DB to Add New recommended Customer Request
class Nominated(db.Model):
    __tablename__ = "nominates"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    nid_or_iq = db.Column(db.BIGINT, nullable=False)
    phone_No = db.Column(db.BIGINT, nullable=False)
    n_visa = db.Column(db.BIGINT, nullable=False)
    n_request_date = db.Column(db.Date, nullable=False)
    worker_name = db.Column(db.String(250), nullable=False)
    worker_contact_No = db.Column(db.BIGINT, nullable=False)
    type = db.Column(db.String(250), nullable=False)
    agency = db.Column(db.String(250), nullable=False)
    selected_or_recommended = db.Column(db.String(250), nullable=False)
    musaned = db.Column(db.String(250), nullable=False)
    embassy_contract = db.Column(db.String(250), nullable=False)
    shipment_date = db.Column(db.Date, nullable=False)
    ppt_image = db.Column(db.String(1000), nullable=False)
    medical = db.Column(db.String(500), nullable=True)
    mmr_vaccine = db.Column(db.String(500), nullable=True)
    owwa = db.Column(db.String(500), nullable=True)
    tesda = db.Column(db.String(500), nullable=True)
    biometric = db.Column(db.String(500), nullable=True)
    stamping = db.Column(db.String(500), nullable=True)
    oec = db.Column(db.String(500), nullable=True)
    ticket = db.Column(db.String(500), nullable=True)
    deployment_date = db.Column(db.String(500), nullable=True)  # Salalim Remarks
    status = db.Column(db.String(1000), nullable=True)


# Creating Table in the DB  to Add new worker Complaint

class Complaint(db.Model):
    __tablename__ = "complaint"
    id = db.Column(db.Integer, primary_key=True)
    worker_name = db.Column(db.String(250), nullable=False)
    Employer_name = db.Column(db.String(250), nullable=False)
    Worker_contact_No = db.Column(db.BIGINT, nullable=False)
    Employer_contact_No = db.Column(db.BIGINT, nullable=False)
    Deployment_Date = db.Column(db.Date, nullable=False)
    Complaint_Description = db.Column(db.String(1000), nullable=False)
    Status = db.Column(db.String(1000), nullable=False)


# CREATE TABLE IN DB To save users login Data (Hashed & Salted)
class User(UserMixin, db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


db.create_all()


# Add Customer Request Flask Form for (السلالم الدولية)
class AddUser(FlaskForm):
    name = StringField('اسم العميل ', validators=[DataRequired(), length(max=100)],
                       description="الرجاء إدخال الاسم باللغة الانجليزية")
    nid_or_iqama = StringField(' الهوية الوطنية أو الإقامة', validators=[DataRequired(), length(max=10)],
                               description="ادخل رقم هوية صالح مكون من 10 ارقام")
    contact_No = StringField('رقم الجوال', validators=[DataRequired()],
                             description='05xxxxxxxx : مثال')
    visa = StringField('رقم التأشيرة', validators=[DataRequired(), length(max=10)],
                       description="ادخل رقم تأشيرة صالح مكون من 10 ارقام")
    request_date = DateField('تاريخ الطلب', validators=[DataRequired()], format='%Y-%m-%d')
    worker_name = StringField('إسم العاملة', validators=[DataRequired(), length(max=150)],
                              description='كما هو مدون في جواز السفر')
    type = SelectField('المهنة',
                       choices=["House Maid", "House Boy", " Private Nurse", "Nanny/Babysitter",
                                " Family Driver"])
    agency = SelectField('المكتب', choices=["Domec", "Myriad", "Reenkam", "TradeFast", "بايونير", "الشريف", "Imran "
                                                                                                            "International"])
    selected_or_recommended = SelectField('معينة ام مختارة', choices=[" Selected"])
    musaned = SelectField('عقد مساند', choices=["  No", "   Yes"])
    embassy_contract = SelectField('عقد السفارة', choices=["  No", "  Yes"])
    shipment_date = DateField(' تاريخ الإرسالية', format='%Y-%m-%d')
    deployment_date = StringField('ملاحظات السلالم الدولية', validators=[length(max=1000)])  # Salalim Remarks
    submit = SubmitField('Submit إضافة')


# Edit Customer Request Flask Form for (السلالم الدولية)
class EditUser(FlaskForm):
    deployment_date = StringField('ملاحظات السلالم الدولية ', validators=[length(max=1000)]) # Salalim Remarks
    submit = SubmitField('تــعـديــل')


class EditMusaned(FlaskForm):
    musaned = SelectField('هل تم تجهيز عقد مساند؟', choices=["  No", "   Yes"])
    submit = SubmitField('تــعـديــل')

class EditConsulate(FlaskForm):
    embassy_contract = SelectField('هل تم تجهيز عقد السفارة', choices=["  No", "  Yes"])
    submit = SubmitField('تــعـديــل')

class EditShipment(FlaskForm):
    shipment_date = DateField('متى تم إرسال العقد للفلبين ؟', format='%Y-%m-%d')
    submit = SubmitField('تــعـديــل')

class EditNominatedMusaned(FlaskForm):
    musaned = SelectField('هل تم تجهيز عقد مساند؟', choices=["  No", "   Yes"])
    submit = SubmitField('تــعـديــل')

class EditNominatedConsulate(FlaskForm):
    embassy_contract = SelectField('هل تم تجهيز عقد السفارة', choices=["  No", "  Yes"])
    submit = SubmitField('تــعـديــل')

class EditNominatedShipment(FlaskForm):
    shipment_date = DateField('متى تم إرسال العقد للفلبين ؟', format='%Y-%m-%d')
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
                                          choices=["Selected", " Recommended"])
    agency = SelectField('المكتب', choices=["Domec", "Myriad", "Reenkam", "TradeFast", "بايونير", "الشريف",
                                            "Imran International", "World Vision Int."])
    jo_status = SelectField('حالة الجوب اوردر', choices=["For POLO Verification", "Verified From POLO and sent Via DHL",
                                                         "For POEA Approval", "POEA Approved",
                                                         "INDIAN IMMIGRATION APPROVED"])
    shipment_date = StringField(' ملاحظات السلالم الدولية', validators=[length(max=1000)])
    submit = SubmitField('Add إضافة')


# Edit new skills Request Flask Form for (السلالم الدولية)

class EditSkills(FlaskForm):
    jo_status = SelectField('حالة الجوب اوردر', choices=["For POLO Verification", "Verified From POLO and sent Via DHL",
                                                         "For POEA Approval", "POEA Approved"])
    shipment_date = StringField(' ملاحظات السلالم الدولية', validators=[length(max=1000)]) # salalim remarks
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
    second_contact_no = IntegerField('رقم جوال الكفيل الثاني', validators=[DataRequired()],
                                     description='ادخل رقم جوال صالح مكون من 10 ارقام ')
    request_date = DateField(' تاريخ الطلب', format='%Y-%m-%d')
    iqama = SelectField(' الإقامة', choices=["نعم", "لا"])
    agency = SelectField('المكتب', choices=["Domec", "Myriad", "Jinhel", "Reenkam", "الصالح", "الشريف "])
    request_status = SelectField('حالة الطلب', choices=["العاملة في فترة التجربة",
                                                        "أكملت العاملة فترة التجربة وجاري إنهاء أجراءات نقل الكفالة",
                                                        "في انتظار سداد رسوم الإقامة / نقل الكفالة",
                                                        "تم نقل الخدمات",
                                                        "العاملة رفضت نقل الكفالة وتراجعت"])
    status = StringField('  ملاحظات ', validators=[DataRequired(), length(max=1000)])
    submit = SubmitField('إضــافـة الطلــب')


# Edit new Transfer Request Flask Form for (السلالم الدولية)
class EditTransfer(FlaskForm):
    iqama = SelectField(' الإقامة', choices=["نعم", "لا"])
    reqeust_status = SelectField('حالة الطلب', choices=["العاملة في فترة التجربة",
                                                        "أكملت العاملة فترة التجربة وجاري إنهاء أجراءات نقل الكفالة",
                                                        "في انتظار سداد رسوم الإقامة / نقل الكفالة",
                                                        "تم نقل الكفالة بنجاح",
                                                        "العاملة رفضت نقل الكفالة وتراجعت"])
    status = StringField('  ملاحظات ', validators=[DataRequired(), length(max=1000)])
    submit = SubmitField('تــعـديــل')


# Add Recommended Customer Request Flask Form for (السلالم الدولية)
class AddNominated(FlaskForm):
    name = StringField('اسم العميل ', validators=[DataRequired(), length(max=100)])
    nid_or_iq = StringField(' الهوية الوطنية أو الإقامة', validators=[DataRequired(), length(max=10)],
                            description="ادخل رقم هوية صالح مكون من 10 ارقام")
    phone_No = StringField('رقم الجوال', validators=[DataRequired()],
                           description='05xxxxxxxx : مثال')
    n_visa = StringField('رقم التأشيرة', validators=[DataRequired(), length(max=10)],
                         description="ادخل رقم تأشيرة صالح مكون من 10 ارقام")
    n_request_date = DateField('تاريخ الطلب', validators=[DataRequired()], format='%Y-%m-%d')
    worker_name = StringField('إسم العاملة', validators=[DataRequired(), length(max=150)],
                              description='كما هو مدون في جواز السفر')

    worker_contact_No = StringField('رقم جوال العاملة', validators=[DataRequired(), length(max=150)],
                                    description='لابد من ان يكون الرقم صحيحاً')
    type = SelectField('المهنة',
                       choices=["House Maid", "House Boy","House Cook"," Private Nurse", "Nanny/Babysitter"," Family Driver","Sewer"])
    agency = SelectField('المكتب', choices=["Domec", "ALZETSI", "Reenkam", "TradeFast"])
    selected_or_recommended = SelectField('معينة ام مختارة',
                                          choices=[" Recommended"])
    musaned = SelectField('عقد مساند', choices=["  No", "   Yes"])
    embassy_contract = SelectField('عقد السفارة', choices=["  No", "  Yes"])
    shipment_date = DateField(' تاريخ الإرسالية', format='%Y-%m-%d')
    ppt_image = StringField('صــورة الـجواز ', validators=[DataRequired(), length(max=2000)])
    # medical = StringField('Medical', validators=[length(max=1000)])
    # mmr_vaccine = StringField('MMR-VACCINE', validators=[length(max=1000)])
    # owwa = StringField('OWWA', validators=[length(max=1000)])
    # tesda = StringField('TESDA', validators=[length(max=1000)])
    # biometric = StringField('Biometric', validators=[length(max=1000)])
    # stamping = StringField('Stamping', validators=[length(max=1000)])
    # oec = StringField('OEC', validators=[length(max=1000)])
    deployment_date = StringField('ملاحظات السلالم الدولية', validators=[length(max=1000)])  # Salalim Remarks
    # status = StringField(' ملاحظات دوميك', validators=[length(max=1000)])
    submit = SubmitField('Submit إضافة')


class EditNominated(FlaskForm):
    # name = StringField('اسم العميل ', validators=[DataRequired(), length(max=100)])
    # nid_or_iq = StringField(' الهوية الوطنية أو الإقامة', validators=[DataRequired(), length(max=10)],
    #                         description="ادخل رقم هوية صالح مكون من 10 ارقام")
    # n_visa = StringField('رقم التأشيرة', validators=[DataRequired(), length(max=10)],
    #                      description="ادخل رقم تأشيرة صالح مكون من 10 ارقام")
    # worker_name = StringField('إسم العاملة', validators=[DataRequired(), length(max=150)],
    #                           description='كما هو مدون في جواز السفر')
    # musaned = SelectField('عقد مساند', choices=["  Yes", "   No"])
    # embassy_contract = SelectField('عقد السفارة', choices=[" Yes", "   No"])
    # shipment_date = DateField(' تاريخ الإرسالية', format='%Y-%m-%d')
    deployment_date = StringField('ملاحظات السلالم الدولية', validators=[length(max=1000)]) # salalim Remarks
    submit = SubmitField('تــعـديــل')


class AddComplaint(FlaskForm):
    worker_name = StringField('اسم العاملة', validators=[length(max=200)])
    Employer_name = StringField('اسم الكفيل', validators=[length(max=200)])
    Worker_contact_No = StringField('رقم جوال العاملة', validators=[length(max=200)])
    Employer_contact_No = StringField(' رقم جوال الكفيل', validators=[length(max=200)])
    Deployment_Date = DateField(' تاريخ الوصول', format='%Y-%m-%d')
    Complaint_Description = StringField(' شكوى العاملة', validators=[length(max=1000)])
    Status = StringField('ملاحظات', validators=[length(max=1000)])
    submit = SubmitField('إضـافــة')


class EditComplaint(FlaskForm):
    Status = StringField('ملاحظات', validators=[length(max=1000)])
    submit = SubmitField('تــعـديـل')


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
    status = StringField('Remarks', validators=[length(max=1000)])
    submit = SubmitField('Submit')


# Edit Worker Status Flask Form for (Domec)

class DomecEditUser(FlaskForm):
    # medical = StringField('Medical', validators=[DataRequired(), length(max=1000)])
    # mmr_vaccine = StringField('MMR-VACCINE', validators=[DataRequired(), length(max=1000)])
    # owwa = StringField('OWWA', validators=[DataRequired(), length(max=1000)])
    # tesda = StringField('TESDA', validators=[DataRequired(), length(max=1000)])
    # biometric = StringField('Biometric', validators=[DataRequired(), length(max=1000)])
    # stamping = StringField('Stamping', validators=[DataRequired(), length(max=1000)])
    # oec = StringField('OEC', validators=[DataRequired(), length(max=1000)])
    # deployment_date = StringField('Deployment Date', validators=[length(max=1000)])
    status = StringField('Domec Remarks', validators=[length(max=1000)])
    submit = SubmitField('Submit Changes')


class DomecEditNominated(FlaskForm):
    # medical = StringField('Medical', validators=[DataRequired(), length(max=1000)])
    # mmr_vaccine = StringField('MMR-Vaccine', validators=[DataRequired(), length(max=1000)])
    # owwa = StringField('OWWA', validators=[DataRequired(), length(max=1000)])
    # tesda = StringField('TESDA', validators=[DataRequired(), length(max=1000)])
    # biometric = StringField('Biometric', validators=[DataRequired(), length(max=1000)])
    # stamping = StringField('Stamping', validators=[DataRequired(), length(max=1000)])
    # oec = StringField('OEC', validators=[DataRequired(), length(max=1000)])
    # deployment_date = StringField('Deployment Date', validators=[DataRequired(), length(max=1000)])
    status = StringField('Domec Remarks', validators=[length(max=1000)])
    submit = SubmitField('Submit Changes')


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
    status = StringField(' Remarks', validators=[length(max=500)])
    submit = SubmitField('Submit')


# Edit new skills Request Flask Form for (Domec)

class DomecEditSkills(FlaskForm):
    jo_status = SelectField('Job Order Status', choices=["For POLO Verification", "Verified From POLO and sent Via DHL",
                                                         "For POEA Approval", "POEA Approved"])
    status = StringField('Domec Remarks', validators=[length(max=1000)])
    submit = SubmitField('Update')


class DomecAddComplaint(FlaskForm):
    worker_name = StringField('Worker Name', validators=[length(max=200)])
    Employer_name = StringField('Employer Name', validators=[length(max=200)])
    Worker_contact_No = StringField('Worker Contact No.', validators=[length(max=200)])
    Employer_contact_No = StringField('Employer Contact No.', validators=[length(max=200)])
    Deployment_Date = DateField(' Deployment Date', format='%Y-%m-%d')
    Complaint_Description = StringField('Complaint Details', validators=[length(max=1000)])
    Status = StringField('Complaint Status', validators=[length(max=1000)])
    submit = SubmitField('Submit')


class DomecEditComplaint(FlaskForm):
    Status = StringField('Remarks', validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateMedical(FlaskForm):
    medical  = StringField("Medical Result", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateVaccine(FlaskForm):
    mmr_vaccine  = StringField("MMR VACCINE", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateOwwa(FlaskForm):
    owwa  = StringField("OWWA", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateTesda(FlaskForm):
    tesda  = StringField("TESDA", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateOec(FlaskForm):
    oec  = StringField("OEC", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateBiometric(FlaskForm):
    biometric  = StringField("Biometric", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateStamping(FlaskForm):
    stamping  = StringField("Visa Stamping", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateTicket(FlaskForm):
    ticket  = StringField("Flight Details/Ticket", validators=[length(max=1000)])
    submit = SubmitField('Submit')



class UpdateNominatedMedical(FlaskForm):
    medical  = StringField("Medical Result", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateNominatedVaccine(FlaskForm):
    mmr_vaccine  = StringField("MMR VACCINE", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateNominatedOwwa(FlaskForm):
    owwa  = StringField("OWWA", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateNominatedTesda(FlaskForm):
    tesda  = StringField("TESDA", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateNominatedOec(FlaskForm):
    oec  = StringField("OEC", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateNominatedBiometric(FlaskForm):
    biometric  = StringField("Biometric", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateNominatedStamping(FlaskForm):
    stamping  = StringField("Visa Stamping", validators=[length(max=1000)])
    submit = SubmitField('Submit')

class UpdateNominatedTicket(FlaskForm):
    ticket  = StringField("Flight Details/Ticket", validators=[length(max=1000)])
    submit = SubmitField('Submit')

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
            flash("الحساب مسجل مسبقاً, فضلا قم بتسجيل الدخول")
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
        flash("تم التسجيل بنجاح, فضلاً قم بالعودة الى الصفحة الرئيسية ومن ثم تسجيل الدخول")
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
            flash("الحساب غير مسجل, الرجاء تسجيل الحساب والدخول مرة أخرى")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('كلمة مرور خاطئة, الرجاء التأكد من كلمة المرور والمحاولة مرة أخرى')
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
    all_users = Users.query.all()
    return render_template("index.html", users=all_users, name=current_user.name, logged_in=True)


@app.route("/skills_index")
@login_required
def skills():
    all_skills = Skilled.query.all()
    return render_template("skills_index.html", skills=all_skills, name=current_user.name, logged_in=True)


@app.route("/transfer_index")
@login_required
def transfer():
    all_transfers = Transfer.query.all()
    return render_template("transfer_index.html", transfers=all_transfers, name=current_user.name, logged_in=True)


@app.route("/nominated_index")
@login_required
def nominated():
    all_nominates = Nominated.query.all()
    return render_template("nominated_index.html", nominates=all_nominates, name=current_user.name, logged_in=True)


@app.route("/complaint_index")
@login_required
def complaint():
    all_complaints = Complaint.query.all()
    return render_template("complaint_index.html", complaints=all_complaints, name=current_user.name, logged_in=True)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddUser()

    if form.validate_on_submit():
        new_customer = Users(
            name=form.name.data,
            nid_or_iqama=form.nid_or_iqama.data,
            contact_No=form.contact_No.data,
            visa=form.visa.data,
            request_date=form.request_date.data,
            worker_name=form.worker_name.data,
            type=form.type.data,
            agency=form.agency.data,
            selected_or_recommended=form.selected_or_recommended.data,
            musaned=form.musaned.data,
            embassy_contract=form.embassy_contract.data,
            shipment_date=form.shipment_date.data,
            # medical=form.medical.data,
            # mmr_vaccine=form.mmr_vaccine.data,
            # owwa=form.owwa.data,
            # tesda=form.tesda.data,
            # biometric=form.biometric.data,
            # stamping=form.stamping.data,
            # oec=form.oec.data,
            deployment_date=form.deployment_date.data,  # salalim Remarks
            # status=form.status.data

        )

        db.session.add(new_customer)
        db.session.commit()
        all_users.append(new_customer)
        flash("✔  تم إضافة طلب العمالة المنزلية بنجاح ")
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
            # status=form.status.data
        )

        db.session.add(new_skills)
        db.session.commit()
        all_skills.append(new_skills)
        flash("✔ تم إضافة طلب العمالة المهنية بنجاح ")
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
            request_date=form.request_date.data,
            agency=form.agency.data,
            request_status=form.request_status.data,
            status=form.status.data,
        )
        db.session.add(new_transfer)
        db.session.commit()
        all_skills.append(new_transfer)
        flash("✔ تم إضافة طلب نقل الخدمة بنجاح ")
        return redirect(url_for('add_transfer'))
    return render_template("transfer_add.html", form=form)


@app.route("/nominated_add", methods=["GET", "POST"])
def add_nominated():
    form = AddNominated()

    if form.validate_on_submit():
        new_nominated = Nominated(
            name=form.name.data,
            nid_or_iq=form.nid_or_iq.data,
            phone_No=form.phone_No.data,
            n_visa=form.n_visa.data,
            n_request_date=form.n_request_date.data,
            worker_name=form.worker_name.data,
            worker_contact_No=form.worker_contact_No.data,
            type=form.type.data,
            agency=form.agency.data,
            selected_or_recommended=form.selected_or_recommended.data,
            musaned=form.musaned.data,
            embassy_contract=form.embassy_contract.data,
            shipment_date=form.shipment_date.data,
            ppt_image=form.ppt_image.data,
            deployment_date=form.deployment_date.data, # Salalim Remarks
            # status=form.status.data

        )

        db.session.add(new_nominated)
        db.session.commit()
        all_users.append(new_nominated)
        flash("✔ تم إضافة طلب العاملة المنزلية المعينة بنجاح ")
        return redirect(url_for('add_nominated'))
    return render_template("nominated_add.html", form=form)


@app.route("/complaint_add", methods=["GET", "POST"])
def add_complaint():
    form = AddComplaint()

    if form.validate_on_submit():
        new_complaint = Complaint(
            worker_name=form.worker_name.data,
            Employer_name=form.Employer_name.data,
            Worker_contact_No=form.Worker_contact_No.data,
            Employer_contact_No=form.Employer_contact_No.data,
            Deployment_Date=form.Deployment_Date.data,
            Complaint_Description=form.Complaint_Description.data,
            Status=form.Status.data
        )

        db.session.add(new_complaint)
        db.session.commit()
        all_users.append(new_complaint)
        flash("تم اضافة الشكوى ✔!!")
        return redirect(url_for('add_complaint'))
    return render_template("complaint_add.html", form=form)


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


@app.route("/nominated_list")
def nominated_list():
    added_nominates = Nominated.query.all()
    return render_template("nominated_list.html", nominates=added_nominates, name=current_user.name)


@app.route("/complaint_list")
def complaint_list():
    added_complaints = Complaint.query.all()
    return render_template("complaint_list.html", complaints=added_complaints, name=current_user.name)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditUser()
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    if form.validate_on_submit():
        updated_user.deployment_date = form.deployment_date.data  # salalim Remarks

        db.session.commit()
        flash("✔ تم تعديل بيانات طلب العمالة المنزلية بنجاح")
        return redirect(url_for('edit'))
    return render_template("edit.html", form=form, user=updated_user,id=user_id)


@app.route("/skills_edit", methods=["GET", "POST"])
def skills_edit():
    form = EditSkills()
    skills_id = request.args.get("id")
    updated_skills = Skilled.query.get(skills_id)
    if form.validate_on_submit():
        updated_skills.jo_status = form.jo_status.data
        updated_skills.shipment_date = form.shipment_date.data
        # updated_skills.status = form.status.data

        db.session.commit()
        flash("✔ تم تعديل حالة طلب العمالة المهنية بنجاح")
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
        flash("✔ تم تعديل  طلب نقل الكفالة بنجاح")
        return redirect(url_for('transfer_edit'))
    return render_template("transfers_edit.html", form=form, transfer=updated_transfers)


@app.route("/nominated_edit", methods=["GET", "POST"])
def nominated_edit():
    form = EditNominated()
    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    if form.validate_on_submit():
        updated_nominated.deployment_date = form.deployment_date.data  # Salalim Remarks
        db.session.commit()
        flash("✔ تم تعديل الطلب بنجاح")
        return redirect(url_for('nominated_edit'))
    return render_template("nominated_edit.html", form=form, nominated=updated_nominated)


@app.route("/complaint_edit", methods=["GET", "POST"])
def complaint_edit():
    form = EditComplaint()
    complaint_id = request.args.get("id")
    updated_complaint = Complaint.query.get(complaint_id)
    if form.validate_on_submit():
        updated_complaint.Status = form.Status.data
        db.session.commit()
        flash("✔ تم تعديل حالة الشكوى بنجاح")
        return redirect(url_for('complaint_edit'))
    return render_template("complaint_edit.html", form=form, complaint=updated_complaint)



@app.route("/customer_procedures",methods=["GET", "POST"])
def customer_procedures():
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    return render_template("customer_procedures.html",user=updated_user)

@app.route("/musaned_contract",methods=["GET", "POST"])
def musaned_contract():
    form = EditMusaned()
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    if form.validate_on_submit():
        updated_user.musaned = form.musaned.data
        db.session.commit()
        flash("✔ تم تعديل حالة العقد بنجاح")
        return redirect(url_for('musaned_contract'))
    return render_template("musaned_edit.html", form=form, user=updated_user)

@app.route("/consulate_contract",methods=["GET", "POST"])
def consulate_contract():
    form = EditConsulate()
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    if form.validate_on_submit():
        updated_user.embassy_contract = form.embassy_contract.data
        db.session.commit()
        flash("✔ تم تعديل حالة العقد بنجاح")
        return redirect(url_for('consulate_contract'))
    return render_template("consulate_edit.html", form=form, user=updated_user)

@app.route("/shipment_date_edit",methods=["GET", "POST"])
def shipment_date_edit():
    form = EditShipment()
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    if form.validate_on_submit():
        updated_user.shipment_date = form.shipment_date.data
        db.session.commit()
        flash("✔ تم تعديل تاريخ ألإرسالية بنجاح")
        return redirect(url_for('shipment_date_edit'))
    return render_template("consulate_edit.html", form=form, user=updated_user)



@app.route("/nominated_customer_procedures", methods=["GET", "POST"])
def nominated_customer_procedures():
    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    return render_template("nominated_customer_procedures.html",nominated=updated_nominated)



@app.route("/musaned_nominated_edit", methods=["GET", "POST"])
def musaned_nominated_edit():
    form = EditNominatedMusaned()
    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    if form.validate_on_submit():
        updated_nominated.musaned = form.musaned.data
        db.session.commit()
        flash("✔ تم تعديل حالة العقد بنجاح")
        return redirect(url_for('musaned_nominated_edit'))
    return render_template("musaned_nominated_edit.html", form=form, nominated=updated_nominated)



@app.route("/consulate_nominated_edit", methods=["GET", "POST"])
def consulate_nominated_edit():
    form = EditNominatedConsulate()
    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    if form.validate_on_submit():
        updated_nominated.embassy_contract = form.embassy_contract.data
        db.session.commit()
        flash("✔ تم تعديل حالة العقد بنجاح")
        return redirect(url_for('consulate_nominated_edit'))
    return render_template("consulate_nominated_edit.html", form=form, nominated=updated_nominated)


@app.route("/nominated_shipment_date_edit",methods=["GET", "POST"])
def nominated_shipment_date_edit():
    form = EditNominatedShipment()
    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    if form.validate_on_submit():
        updated_nominated.shipment_date = form.shipment_date.data
        db.session.commit()
        flash("✔ تم تعديل تاريخ ألإرسالية بنجاح")
        return redirect(url_for('nominated_shipment_date_edit'))
    return render_template("nominated_shipment_date_edit.html", form=form, nominated=updated_nominated)













@app.route("/delete")
def delete():
    user_id = request.args.get("id")
    user_to_delete = Users.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("✔ تم حذف بيانات العميل بنجاح")
    return redirect(url_for('users_list'))


@app.route("/skills_delete")
def skills_delete():
    skills_id = request.args.get("id")
    skills_to_delete = Skilled.query.get(skills_id)
    db.session.delete(skills_to_delete)
    db.session.commit()
    flash("✔ تم حذف بيانات طلب العمالة المهنية بنجاح")
    return redirect(url_for('skills_list'))


@app.route("/transfer_delete")
def transfer_delete():
    transfer_id = request.args.get("id")
    transfers_to_delete = Transfer.query.get(transfer_id)
    db.session.delete(transfers_to_delete)
    db.session.commit()
    flash("تم حذف بيانات طلب نقل الخدمة بنجاح✔")
    return redirect(url_for('transfer_list'))


@app.route("/nominated_delete")
def nominated_delete():
    nominated_id = request.args.get("id")
    nominated_to_delete = Nominated.query.get(nominated_id)
    db.session.delete(nominated_to_delete)
    db.session.commit()
    flash("✔ تم حذف بيانات الطلب بنجاح")
    return redirect(url_for('nominated_list'))


@app.route("/complaint_delete")
def complaint_delete():
    complaint_id = request.args.get("id")
    complaint_to_delete = Complaint.query.get(complaint_id)
    db.session.delete(complaint_to_delete)
    db.session.commit()
    flash("✔ تم حذف الشكوى بنجاح")
    return redirect(url_for('complaint_list'))


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


@app.route("/nominated_tables")
def nominated_tables():
    added_nominates = Nominated.query.all()
    return render_template("nominated_tables.html", nominates=added_nominates, name=current_user.name, logged_in=True)


@app.route("/complaint_tables")
def complaint_tables():
    added_complaints = Complaint.query.all()
    return render_template("complaint_tables.html", complaints=added_complaints, name=current_user.name, logged_in=True)


@app.route("/conditions")
def conditions():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/download")
def download():
    return send_from_directory('static', filename="files/user's manual.pdf")

@app.route("/procedures")
def procedures():
    added_users = Users.query.all()
    return render_template("procedures.html",users=added_users, name=current_user.name, logged_in=True)
@ app.route("/nominated-procedures")
def nominated_procedures():
    added_nominates = Nominated.query.all()
    return render_template("nominated_procedures.html",nominates=added_nominates,name=current_user.name, logged_in=True)


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
        flash("Registered Successfully,Please Log in Again")
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
    all_users = Users.query.all()
    return render_template("domec_index.html", users=all_users, name=current_user.name, logged_in=True)


@app.route("/domec-nominated-index.html")
@login_required
def domec_nominated_home():
    all_nominates = Nominated.query.all()
    return render_template("domec_nominated_index.html", nominates=all_nominates, name=current_user.name,
                           logged_in=True)


@app.route("/dom_skills_index.html")
@login_required
def dom_skills():
    all_skills = Skilled.query.all()
    return render_template("dom_skills_index.html", skills=all_skills, name=current_user.name, logged_in=True)


@app.route("/dom_complaint_index.html")
@login_required
def dom_complaint():
    all_complaints = Complaint.query.all()
    return render_template("dom_complaint_index.html", complaints=all_complaints, name=current_user.name,
                           logged_in=True)


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
        flash("Request Added successfully ✔!!")
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


@app.route("/domec_add_complaint", methods=["GET", "POST"])
def domec_add_complaint():
    form = DomecAddComplaint()

    if form.validate_on_submit():
        new_complaint = Complaint(
            worker_name=form.worker_name.data,
            Employer_name=form.Employer_name.data,
            Worker_contact_No=form.Worker_contact_No.data,
            Employer_contact_No=form.Employer_contact_No.data,
            Deployment_Date=form.Deployment_Date.data,
            Complaint_Description=form.Complaint_Description.data,
            Status=form.Status.data
        )
        db.session.add(new_complaint)
        db.session.commit()
        all_users.append(new_complaint)
        flash(" New Complaint Added successfully ✔")
        return redirect(url_for('domec_add_complaint'))
    return render_template("dom_complaint_add.html", form=form)


@app.route("/domec_list")
def domec_users_list():
    added_users = Users.query.all()
    return render_template("domec_list.html", users=added_users, name=current_user.name)


@app.route("/domec_skills_list")
def domec_skills_list():
    added_skills = Skilled.query.all()
    return render_template("dom_skills_list.html", skills=added_skills, name=current_user.name)


@app.route("/domec_nominated_list")
def domec_nominated_list():
    added_nominates = Nominated.query.all()
    return render_template("domec_nominated_list.html", nominates=added_nominates, name=current_user.name)


@app.route("/domec_complaint_list")
def domec_complaint_list():
    added_complaints = Complaint.query.all()
    return render_template("domec_complaint_list.html", complaints=added_complaints, name=current_user.name)


@app.route("/domec_edit", methods=["GET", "POST"])
def domec_edit():
    form = DomecEditUser()
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    if form.validate_on_submit():
        # updated_user.medical = form.medical.data
        # updated_user.mmr_vaccine = form.mmr_vaccine.data
        # updated_user.owwa = form.owwa.data
        # updated_user.tesda = form.tesda.data
        # updated_user.biometric = form.biometric.data
        # updated_user.stamping = form.stamping.data
        # updated_user.oec = form.oec.data
        # updated_user.deployment_date = form.deployment_date.data
        updated_user.status = form.status.data
        db.session.commit()
        flash("Request Modified successfully  ✔")
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


@app.route("/domec_edit_nominated", methods=["GET", "POST"])
def domec_edit_nominated():
    form = DomecEditNominated()
    nominated_id = request.args.get("id")
    updated_nominates = Nominated.query.get(nominated_id)
    if form.validate_on_submit():
        updated_nominates.status = form.status.data
        db.session.commit()
        flash("Request Modified successfully  ✔")
        return redirect(url_for('domec_edit_nominated'))
    return render_template("domec_edit_nominated.html", form=form, nominated=updated_nominates)


@app.route("/domec_edit_complaint", methods=["GET", "POST"])
def domec_edit_complaint():
    form = DomecEditComplaint()
    complaint_id = request.args.get("id")
    updated_complaints = Complaint.query.get(complaint_id)
    if form.validate_on_submit():
        updated_complaints.Status = form.Status.data
        db.session.commit()
        flash("Status successfully Changed ✔")
        return redirect(url_for('domec_edit_complaint'))
    return render_template("domec_edit_complaint.html", form=form, complaint=updated_complaints)

#The main edit page for the procedures
@app.route("/domec_edit_procedures",methods=["GET", "POST"])
def domec_edit_procedures():
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    return render_template("domec_procedures_edit.html",user=updated_user)

@app.route("/medical_update", methods=["GET", "POST"])
def medical_update():

    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    form = UpdateMedical()
    if form.validate_on_submit():
        updated_user.medical = form.medical.data
        db.session.commit()
        flash("Medical Status successfully Changed ✔")
        return redirect(url_for('medical_update'))

    return render_template("medical_edit.html", form=form, user=updated_user)


@app.route("/vaccine_update", methods=["GET", "POST"])
def vaccine_update():
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    form = UpdateVaccine()
    if form.validate_on_submit():
        updated_user.mmr_vaccine = form.mmr_vaccine.data
        db.session.commit()
        flash("MMR Vaccine Status Changed successfully  ✔")
        return redirect(url_for('vaccine_update'))

    return render_template("vaccine_edit.html", form=form, user=updated_user)

@app.route("/owwa_update", methods=["GET", "POST"])
def owwa_update():
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    form = UpdateOwwa()
    if form.validate_on_submit():
        updated_user.owwa = form.owwa.data
        db.session.commit()
        flash(" OWWA Process Status Changed successfully  ✔")
        return redirect(url_for('owwa_update'))

    return render_template("owwa_edit.html", form=form, user=updated_user)

@app.route("/tesda_update", methods=["GET", "POST"])
def tesda_update():
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    form = UpdateTesda()
    if form.validate_on_submit():
        updated_user.tesda = form.tesda.data
        db.session.commit()
        flash(" TESDA Process Status Changed successfully  ✔")
        return redirect(url_for('tesda_update'))

    return render_template("tesda_edit.html", form=form, user=updated_user)


@app.route("/oec_update", methods=["GET", "POST"])
def oec_update():
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    form = UpdateOec()
    if form.validate_on_submit():
        updated_user.oec = form.oec.data
        db.session.commit()
        flash(" OEC Process Status Changed successfully  ✔")
        return redirect(url_for('oec_update'))

    return render_template("oec_edit.html", form=form, user=updated_user)


@app.route("/biometric_update", methods=["GET", "POST"])
def biometric_update():
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    form = UpdateBiometric()
    if form.validate_on_submit():
        updated_user.biometric = form.biometric.data
        db.session.commit()
        flash(" Biometric Process Status Changed successfully  ✔")
        return redirect(url_for('biometric_update'))

    return render_template("biometric_edit.html", form=form, user=updated_user)


@app.route("/stamping_update", methods=["GET", "POST"])
def stamping_update():
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    form = UpdateStamping()
    if form.validate_on_submit():
        updated_user.stamping = form.stamping.data
        db.session.commit()
        flash(" Visa Stamping Process Status Changed successfully  ✔")
        return redirect(url_for('stamping_update'))

    return render_template("stamping_edit.html", form=form, user=updated_user)

@app.route("/ticket_update", methods=["GET", "POST"])
def ticket_update():
    user_id = request.args.get("id")
    updated_user = Users.query.get(user_id)
    form = UpdateTicket()
    if form.validate_on_submit():
        updated_user.ticket = form.ticket.data
        db.session.commit()
        flash(" Flight Details Process Status Changed successfully  ✔")
        return redirect(url_for('ticket_update'))

    return render_template("ticket_edit.html", form=form, user=updated_user)



@app.route("/domec_edit_nominated_procedures",methods=["GET", "POST"])
def domec_edit_nominated_procedures():
    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    return render_template("domec_nominated_procedures_edit.html",nominated=updated_nominated)

@app.route("/nominated_medical_update", methods=["GET", "POST"])
def nominated_medical_update():

    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    form = UpdateNominatedMedical()
    if form.validate_on_submit():
        updated_nominated.medical = form.medical.data
        db.session.commit()
        flash("Medical Status successfully Changed ✔")
        return redirect(url_for('nominated_medical_update'))

    return render_template("nominated_medical_edit.html", form=form, nominated=updated_nominated)

@app.route("/nominated_vaccine_update", methods=["GET", "POST"])
def nominated_vaccine_update():

    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    form = UpdateNominatedVaccine()
    if form.validate_on_submit():
        updated_nominated.mmr_vaccine = form.mmr_vaccine.data
        db.session.commit()
        flash("MMR Vaccine Status successfully Changed ✔")
        return redirect(url_for('nominated_vaccine_update'))

    return render_template("nominated_vaccine_edit.html", form=form, nominated=updated_nominated)

@app.route("/nominated_owwa_update", methods=["GET", "POST"])
def nominated_owwa_update():

    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    form = UpdateNominatedOwwa()
    if form.validate_on_submit():
        updated_nominated.owwa = form.owwa.data
        db.session.commit()
        flash("OWWA Status successfully Changed ✔")
        return redirect(url_for('nominated_owwa_update'))

    return render_template("nominated_owwa_edit.html", form=form, nominated=updated_nominated)

@app.route("/nominated_tesda_update", methods=["GET", "POST"])
def nominated_tesda_update():

    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    form = UpdateNominatedTesda()
    if form.validate_on_submit():
        updated_nominated.tesda = form.tesda.data
        db.session.commit()
        flash("TESDA Status successfully Changed ✔")
        return redirect(url_for('nominated_tesda_update'))

    return render_template("nominated_tesda_edit.html", form=form, nominated=updated_nominated)

@app.route("/nominated_oec_update", methods=["GET", "POST"])
def nominated_oec_update():

    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    form = UpdateNominatedOec()
    if form.validate_on_submit():
        updated_nominated.oec = form.oec.data
        db.session.commit()
        flash("OEC Status successfully Changed ✔")
        return redirect(url_for('nominated_oec_update'))

    return render_template("nominated_oec_edit.html", form=form, nominated=updated_nominated)

@app.route("/nominated_biometric_update", methods=["GET", "POST"])
def nominated_biometric_update():

    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    form = UpdateNominatedBiometric()
    if form.validate_on_submit():
        updated_nominated.biometric = form.biometric.data
        db.session.commit()
        flash("BIOMETRIC Status successfully Changed ✔")
        return redirect(url_for('nominated_biometric_update'))

    return render_template("nominated_biometric_edit.html", form=form, nominated=updated_nominated)

@app.route("/nominated_stamping_update", methods=["GET", "POST"])
def nominated_stamping_update():

    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    form = UpdateNominatedStamping()
    if form.validate_on_submit():
        updated_nominated.stamping = form.stamping.data
        db.session.commit()
        flash("Stamping Status successfully Changed ✔")
        return redirect(url_for('nominated_stamping_update'))

    return render_template("nominated_stamping_edit.html", form=form, nominated=updated_nominated)

@app.route("/nominated_ticket_update", methods=["GET", "POST"])
def nominated_ticket_update():

    nominated_id = request.args.get("id")
    updated_nominated = Nominated.query.get(nominated_id)
    form = UpdateNominatedTicket()
    if form.validate_on_submit():
        updated_nominated.ticket = form.ticket.data
        db.session.commit()
        flash("Ticket Status successfully Changed ✔")
        return redirect(url_for('nominated_ticket_update'))

    return render_template("nominated_ticket_edit.html", form=form, nominated=updated_nominated)



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


@app.route("/domec_nominated_tables")
def domec_nominated_tables():
    added_nominates = Nominated.query.all()
    return render_template("domec_nominated_tables.html", nominates=added_nominates, name=current_user.name,
                           logged_in=True)


@app.route("/domec_complaints_tables")
def domec_complaints_tables():
    added_complaints = Complaint.query.all()
    return render_template("dom_complaints_tables.html", complaints=added_complaints, name=current_user.name,
                           logged_in=True)

@app.route("/domec_procedures")
@login_required
def domec_procedures():
    all_users = Users.query.all()
    return render_template("domec-procedures.html", users=all_users, name=current_user.name, logged_in=True)

@app.route("/domec_nominated_procedures")
@login_required
def domec_nominated_procedures():
    all_nominates = Nominated.query.all()
    return render_template("domec_nominated_procedures.html", nominates=all_nominates, name=current_user.name,
                           logged_in=True)


########################################################################################################################


if __name__ == "__main__":
    app.run(debug=True)
