from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt

import helper

# Initialize app
app = Flask(__name__)
app.config["debug"] = True


# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{host}/{database}".format(
#     username='gin040',
#     password='mydb%pw>3!',
#     host='gin040.mysql.pythonanywhere-services.com',
#     database='gin040$mydb')
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'

app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'secretkey'

db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Create username"})
    email = EmailField(validators=[InputRequired(), Length(
    min=4, max=20), Email()], render_kw={"placeholder": "Create password"})
    password = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Create password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class SolarcalcForm(FlaskForm):
    num = StringField(validators=[InputRequired(), Length(
        min=1, max=5)], render_kw={"placeholder": "Aantal zonnepanelen"})
    wp = StringField(validators=[InputRequired(), Length(
        min=1, max=4)], render_kw={"placeholder": "Wattpiek"})
    lat = StringField(validators=[InputRequired(), Length(
        min=1, max=3)], render_kw={"placeholder": "Latitude"})
    lon = StringField(validators=[InputRequired(), Length(
        min=1, max=3)], render_kw={"placeholder": "Longitude"})
    submit = SubmitField("Bereken")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/energypv')
def energypv():
    return render_template("energy-pv.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        with app.app_context():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template("login.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/pvcalculator", methods=["GET", "POST"])
@login_required
def pvcalculator():
    form = SolarcalcForm()
    return render_template("pvcalculator.html", form=form)


@app.route("/resultaat", methods=["GET", "POST"])
@login_required
def resultaat():
    num = request.form.get("num", type=int)
    wp = request.form.get("wp", type=int)
    lat = request.form.get("lat", type=float)
    lon = request.form.get("lon", type=float)
    res = helper.solarcalc(num, wp, lat_deg = lat, lon_deg = lon)
    return render_template("pvresult.html", res=res)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
