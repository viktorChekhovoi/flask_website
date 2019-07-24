from firstapp import app
from flask import render_template
from firstapp.login_form import Login_Form
import requests
import json

@app.route('/')
@app.route('/index')
def index():
    url = "https://api.github.com/users/victorChekhovoy/events"
    r = requests.get(url)
    response = r.json()

    for a in response:
        if a['type'] == 'PushEvent':
            last = a
            break
    username = 'pictor'
    return render_template('index.html', user=username, date = last['created_at'])


@app.route('/login')
def login():
    form = Login_Form()
    return render_template('login.html',title = 'sign in',  login_form = form)
