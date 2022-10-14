from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'   # db = name of the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY")
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    todo_list = Todo.query.all()

    if session['username']:
        username = session['username']
    else:
        username = ''

    if len(todo_list) > 0:
        return render_template('base.html', todo_list=todo_list, username=username)
    else:
        return render_template('base.html', todo_list=todo_list, username=username)

@app.route('/clear_all', methods=['POST'])
def clear_all():
    try:
        db.session.query(Todo).delete()
        db.session.commit()
        print('Items deleted!')
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        print(f'TODOS NOT DELETED! \n Error: {e}')
        return redirect(url_for('index'))
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        session['password'] = password
        if username == 'Maria' and password == '123':
            return redirect(url_for('todos'))
        else:
            return render_template('login.html') + f"<h2 style='text-align: center; color: black;'>Wrong username or password. <br/> Please, check your data!</h2>"
    else:
        return render_template('login.html')
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/todos')
def todos():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('index', username=username))
    else:
        return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)


## https://www.youtube.com/watch?v=1nxzOrLWiic&list=TLPQMTAxMDIwMjKLYp3YZnvhxg&index=8
"""
comandos para rodar o flask: na sequencia em que aparecem abaixo
export FLASK_APP=app.py          ## especifica como rodar a aplicação
export FLASK_ENV=development     ## define o tipo de execução do projeto (desenvolvimento ou produção)
flask run
após isso e if __name__ == '__main__', roda o projeto normalmente (python3 app.py)
"""
