from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_required, current_user, logout_user, LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/becke/PycharmProjects/Day 88/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
    return user


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, id, name, email, password):
        __tablename__ = "Users"
        self.id = id
        self.name = name
        self.email = email
        self.password = password


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    is_done = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_competed = db.Column(db.DateTime, nullable=True)

    def __init__(self, id, user, name, description, is_done, date_created, date_completed):
        __tablename__ = "todos"
        self.id = id
        self.user = user
        self.name = name
        self.description = description
        self.is_done = is_done
        self.date_created = date_created
        self.date_competed = date_completed


@app.route("/")
def home_page():
    current_todos = []
    if current_user.is_authenticated:
        with app.app_context():
            current_todos = ToDo.query.filter_by(user_id=current_user.id).all()
            user = current_user
    else:
        user = []
    return render_template("index.html", todos=current_todos, user=user)


@app.route("/add_to_do", methods=["GET", "POST"])
def add_to_do():
    form = ToDoForm()
    if current_user.is_authenticated:
        if request.method == "GET":
            return render_template("add_to_do.html", form=form)
        elif request.method == "POST":
            with app.app_context():
                new_id = len(ToDo.query.all())
            new_task = form.name.data
            new_description = form.description.data
            new_is_done = form.is_done.data
            new_date_created = datetime.today()
            new_todo = ToDo(
                id=new_id,
                user=current_user.id,
                name=new_task,
                description=new_description,
                is_done=new_is_done,
                date_created=new_date_created,
                date_completed=new_date_created
            )
            with app.app_context():
                db.session.add(new_todo)
                db.session.commit()
            return render_template("success.html", task=new_task)
    else:
        return redirect(url_for("login"))


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    form = UserForm()
    if request.method == "GET":
        return render_template("add_to_do.html", form=form)
    elif request.method == "POST":
        with app.app_context():
            new_id = len(User.query.all()) + 1
        new_name = form.name.data.title()
        new_email = form.email.data.lower()
        new_password = generate_password_hash(form.password.data, method="sha256", salt_length=16)
        new_user = User(id=new_id, name=new_name, email=new_email, password=new_password)
        with app.app_context():
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()
        return render_template("success.html", task=new_name)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "GET":
        return render_template("login_form.html", form=login_form)
    elif request.method == "POST":
        email_input = login_form.email.data.lower()
        with app.app_context():
            requested_user = User.query.filter_by(email=email_input).first()
            print(requested_user.name)
        if check_password_hash(requested_user.password, login_form.password.data):
            login_user(requested_user)
            return render_template("login_success.html")
    else:
        return "Login Failure"


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return "you have successfully logged out"
    else:
        flash(message="You are not currently logged in", category="message")
        return redirect(url_for("home_page"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
