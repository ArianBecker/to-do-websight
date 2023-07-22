from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/becke/PycharmProjects/Day 88/to_do.df'
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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
