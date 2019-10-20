from flask import Flask, request, url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__, static_url_path='/static')

# Configuring Database
file = yaml.load(open('/home/titanconnect/titanconnect/db.yaml'))
app.config['MYSQL_HOST'] = file['mysql_host']
app.config['MYSQL_USER'] = file['mysql_user']
app.config['MYSQL_PASSWORD'] = file['mysql_password']
app.config['MYSQL_DB'] = file['mysql_db']

mysql = MySQL(app)

@app.route('/')
def home_page():
    return app.send_static_file('index.html')

@app.route('/index.html')
def index():
    return app.send_static_file('index.html')

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO accounts(username, email, password) VALUES(%s, %s, %s)",(email, email, password))
        mysql.connection.commit()
        cur.close()

    return app.send_static_file('signup.html')

@app.route('/newpost.html')
def newpost():
    return app.send_static_file('newpost.html')

@app.route('/profile.html')
def profile():
    return app.send_static_file('profile.html')

@app.route('/login.html', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from accounts  where username = %s AND password = %s",(username, password))
        result = cur.fetchall()
        if cur.rowcount == 1 and result[0][0] == username and result[0][2] == password:
            return "log in successfull"
        return "log in failed"
    return app.send_static_file('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('Username:' + request.form['email'] + ' password' + request.form['password'])
        return 'Username:' + request.form['email'] + ' password' + request.form['password']
