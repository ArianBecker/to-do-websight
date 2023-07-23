from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_required, current_user, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/becke/PycharmProjects/Day 88/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
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
    return render_template("index.html")


@app.route("/add_to_do", methods=["GET", "POST"])
def add_to_do():
    form = ToDoForm()
    if request.method == "GET":
        return render_template("add_to_do.html", form=form)
    elif request.method == "POST":
        new_task = form.name.data
        new_description = form.description.data
        new_is_done = form.is_done.data
        new_date_created = datetime.today()
        with app.app_context():
            pass
        return render_template("success.html", task=new_task)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    form = UserForm()
    if request.method == "GET":
        return render_template("add_to_do.html", form=form)
    elif request.method == "POST":
        with app.app_context():
            new_id = len(User.query.all()) + 1
        new_name = form.name.data
        new_email = form.email.data
        new_password = generate_password_hash(form.password.data, method="sha256", salt_length=16)
        new_user = User(id=new_id, name=new_name, email=new_email, password=new_password)
        with app.app_context():
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()
        return render_template("success.html", task=new_name)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
