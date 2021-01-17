from flask import Flask, flash, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'Todo.db')
db = SQLAlchemy(app)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    content = request.form.get('content')
    if not title or not content:
        flash('title ve detay girmelisin!', "error")
        return redirect(url_for('index'))
    else:
        newTodo = Todo(title=title, content=content)
        db.session.add(newTodo)
        db.session.commit()
        return redirect(url_for('index'))


@app.route("/completed/<string:job_id>")
def completeTodo(job_id):
    todo = Todo.query.filter_by(id=job_id).first()
    if todo.complete == False:
        todo.complete = True
    else:
        todo.complete = False

    db.session.commit()
    return redirect(url_for('index'))


@app.route('/deleted/<string:job_id>')
def deleted(job_id):
    todo = Todo.query.filter_by(id=job_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/Job/<string:job_id>')
def Detail(job_id):
    todo = Todo.query.filter_by(id=job_id).first()
    return render_template('detail.html', todo=todo)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean, default=False)


if __name__ == '__main__':
    app.run()
