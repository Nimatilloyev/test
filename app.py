from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = "asdadawdawd"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class Subjects(db.Model):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subjects_name = Column(String)
    levels = db.relationship("Levels", backref="subjects", order_by="Levels.id")
    answers = db.relationship("Answers", backref="subjects", order_by="Answers.id")
    questions = db.relationship("Questions", backref="subjects", order_by="Questions.id")


class Levels(db.Model):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True)
    subjects_id = Column(Integer, ForeignKey("subjects.id"))
    name = Column(String)
    questions = db.relationship("Questions", backref="levels", order_by="Questions.id")
    answers = db.relationship("Answers", backref="levels", order_by="Answers.id")


class Questions(db.Model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    questions = Column(String)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    level_id = Column(Integer, ForeignKey("levels.id"))
    answers = db.relationship("Answers", backref="question", order_by="Answers.id")


class Answers(db.Model):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    answers = Column(String)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    level_id = Column(Integer, ForeignKey("levels.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))


@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route('/test')
def test():
    if request.method == "POST":
        return redirect(url_for("test"))
    subjects = Subjects.query.order_by(Subjects.id).all()
    return render_template("test.html", subjects=subjects)


@app.route('/create_subjects', methods=["GET", "POST"])
def create_subjects():
    if request.method == "POST":
        subjects_name = request.form.get("subjects_name")
        add = Subjects(subjects_name=subjects_name)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('create_subjects'))
    return render_template("create_subjects.html")


@app.route('/add_levels', methods=["GET", "POST"])
def add_levels():
    if request.method == "POST":
        name = request.form.get("name")
        subjects_id = request.form.get("subjects_id")
        add = Levels(name=name, subjects_id=subjects_id)
        db.session.add(add)
        db.session.commit()
        subjects = Subjects.query.filter(Subjects.id == subjects_id).first()
        subjects.levels.append(add)
        db.session.commit()
        return redirect(url_for('add_levels'))
    subjects = Subjects.query.order_by(Subjects.id).all()
    return render_template("add_levels.html", subjects=subjects)


@app.route('/levels', methods=["POST", "GET"])
def levels():
    # if request.method == "POST":
    levels = Levels.query.order_by(Levels.id).all()
    return render_template("levels.html", levels=levels)



# @app.route('/')
# def

# subject
@app.route('/english')
def english():
    return render_template("subjects/english.html")


# levels
@app.route('/beginner')
def beginner():
    return render_template("levels/beginner.html")


if __name__ == '__main__':
    app.run()
