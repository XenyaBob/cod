from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from tkinter import *
from tkcalendar import Calendar
import random


app = Flask(__name__) #создаём объект на основе класса Flask, передаём название основного файла (app.py)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean)


class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text, nullable=False)
    nom = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Quotes %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    with open('templates/quotes.txt', encoding="UTF-8") as f:
        if request.method == 'GET':
            n = random.randint(0, 11)
            n *= 2
            k = 0
            for line in f:
                if k == n:
                    line1 = line
                elif k == n + 1:
                    return render_template('index.html', incomplete=incomplete, complete=complete, line1=line1, line=line)
                k += 1


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    #остаемся на главной странице
    return redirect(url_for('index'))


@app.route('/incomplete/<id>')
def incomplete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = False
    db.session.commit()
    #остаемся на главной странице
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()
    #остаемся на главной странице
    return redirect(url_for('index'))

@app.route('/update/<id>')
def update(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.update(todo)

    db.session.commit()
    #остаемся на главной странице
    return redirect(url_for('index'))


#calender- to choose
root = Tk()
root.geometry("400x400")
cal = Calendar(root, selectmode='day',
               year=2022, month=5,
               day=7)

cal.pack(pady=20)

def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())
Button(root, text="Get Date",
       command=grad_date).pack(pady=20)

date = Label(root, text="")
date.pack(pady=20)
root.mainloop()


if __name__ == '__main__':
    app.run(debug = True) #потом надо будет сделать False
