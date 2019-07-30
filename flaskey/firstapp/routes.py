from firstapp import app, db
from flask import render_template, redirect, flash, url_for, request
from firstapp.login_form import Login_Form, Registration_Form
import requests
import json
from flask_login import current_user, login_user, logout_user, login_required
from firstapp.models import User
from werkzeug.urls import url_parse
@app.route('/')
@app.route('/index')
@login_required
def index():
    url = "https://api.github.com/users/victorChekhovoy/events"
    r = requests.get(url)
    response = r.json()

    for a in response:
        if a['type'] == 'PushEvent':
            last = a
            break

    return render_template('index.html', date = last['created_at'])


@app.route('/login', methods = ['GET', 'POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = Login_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html',title = 'sign in',  login_form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/registration', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Registration_Form()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', form = form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)
