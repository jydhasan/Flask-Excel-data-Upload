from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# secret key for flash messages
app.config['SECRET_KEY'] = '1234567'
db = SQLAlchemy(app)
# create db model


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))


def __self__(self, name, age, email):
    self.name = name
    self.age = age
    self.email = email


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/students')
def students():
    students = Students.query.all()
    return render_template('students.html', students=students)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        student = Students(name=name, age=age, email=email)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully')
        return redirect(url_for('students'))
    else:
        return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # save excel data to database
    if request.method == 'POST':
        file = request.files['inputFile']
        file.save(file.filename)
        df = pd.read_excel(file.filename)
        df.to_sql('students', con=db.engine, if_exists='replace', index=False)
        return redirect(url_for('students'))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
