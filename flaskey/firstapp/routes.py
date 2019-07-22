from firstapp import app

@app.route('/')
@app.route('/index')
def index():
    return "henlo!"
