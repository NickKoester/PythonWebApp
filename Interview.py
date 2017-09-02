from flask import Flask, render_template, request, session, flash
import os
from sheetAppend import sheetAppend
from sqlalchemy.orm import sessionmaker
from tabledef import create_engine, User
engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session['username'] == 'admin':
        return render_template('admin.html')
    else:
        return render_template('form.html')


@app.route('/login', methods=['POST'])
def login():
    post_username= str(request.form['username'])
    post_password= str(request.form['password'])

    Session=sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([post_username]), User.password.in_([post_password]))
    result = query.first()
    if result:
        session['logged_in'] = True
        session['username'] = post_username
    else:
        flash('Invalid username or password.')
    return index()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route('/confirm', methods=['POST', 'GET'])
def confirm():
    if request.method == 'POST':
        result = request.form
        sheetAppend(list(result.values()))
        return render_template('confirm.html', result=result)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run()
