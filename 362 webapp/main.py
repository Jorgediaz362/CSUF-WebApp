from flask import Flask, request, url_for

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home_page():
    return app.send_static_file('index.html')

@app.route('/index.html')
def index():
    return app.send_static_file('index.html')

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return 'Username:' + request.form['email'] + ' password' + request.form['password']
    return app.send_static_file('signup.html')

@app.route('/forum.html')
def forum():
    return app.send_static_file('forum.html')

@app.route('/login.html')
def login():
    return app.send_static_file('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return 'Username:' + request.form['email'] + ' password' + request.form['password']
        
