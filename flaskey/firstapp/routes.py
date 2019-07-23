from firstapp import app
from flask import render_template
@app.route('/')
@app.route('/index')
def index():
    username = 'pictor'
    return render_template('index.html', user=username)

