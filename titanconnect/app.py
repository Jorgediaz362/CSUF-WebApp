from flask import Flask, request, url_for, render_template, redirect, session, g
from flask_mysqldb import MySQL
import secrets
import smtplib
import yaml
import os
import json


#import bcrypt
#from hashlib.hash import sha256_crypt as sha256
from passlib.hash import sha256_crypt
#from hashlib.hash import sha256_crypt

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)


logged_in = False;

# Configuring Database
file = yaml.load(open('/home/titanconnect/titanconnect/db.yaml'))
app.config['MYSQL_HOST'] = file['mysql_host']
app.config['MYSQL_USER'] = file['mysql_user']
app.config['MYSQL_PASSWORD'] = file['mysql_password']
app.config['MYSQL_DB'] = file['mysql_db']

mysql = MySQL(app)

@app.route('/')
def home_page():
    print("home route")
    print("method = " + str(request.method))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts ORDER BY time_posted DESC")
    data = cur.fetchall()
    #cur.close()
    cur.execute('SELECT * FROM posts WHERE email = %s ORDER BY time_posted DESC LIMIT 3', (g.user,))
    recentPosts = cur.fetchall()

    cur.close()
    return render_template('home.html', logged_in=logged_in,data=data,recentPosts=recentPosts)

@app.route('/index.html')
def index():
    return app.send_static_file('index.html')

#check session before running any requests
@app.before_request
def before_request():
    #global var to track a single person across different threads on a server
    g.user = None
    if 'user' in session:
        g.user = session['user']
        #g.user = g.user.split("@", 1)[0]



@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        password = sha256_crypt.encrypt(password)
        #print (pass1)
        #return ""
        token = secrets.token_hex(6)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO accounts(username, email, password, token) VALUES(%s, %s, %s, %s)",(email, email, password, token))

        mysql.connection.commit()
        cur.close()

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("titianconnect", "f@vZHtizz")
        server.sendmail(
            "titianconnect@gmail.com",
            email,
            token)
        server.quit()
        return app.send_static_file('verify.html')

    return app.send_static_file('signup.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':

       token = request.form['token']
       cur = mysql.connection.cursor()
       cur.execute("UPDATE accounts SET registered = 1 WHERE token = %s", (1, token))
       mysql.connection.commit()
       cur.close()

    return app.send_static_file('login.html')

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    #check if session is active. only logged in users can create new posts
    if request.method == 'GET':
        if g.user:
            #return app.send_static_file('newpost.html')
            return render_template('newpost.html')
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.json['title']
        description = request.json['description']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts(email, title, description, time_posted) VALUES(%s, %s, %s, now())",(session['user'], title, description))
        mysql.connection.commit()
        cur.close()
    return render_template('home.html', logged_in=True,name=session['user'])


@app.route('/profile')
def profile():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM posts WHERE email = %s ORDER BY time_posted DESC", (g.user,))
    myPosts = cur.fetchall()
    cur.close()
    return render_template('profile.html',logged_in=True, name=session['user'],myPosts=myPosts)

@app.route('/users/<users>')
def users(users):

    users = users
    userEmail = users + "@csu.fullerton.edu"

    cur = mysql.connection.cursor()
    cur.execute("select * from posts where email = %s or email = %s order by time_posted desc ", (users,userEmail))
    usersPosts = cur.fetchall()
    cur.close()
    return render_template('users.html',users=users,userEmail=userEmail,usersPosts=usersPosts)


@app.route('/login.html', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        username = request.json['username']
        password = request.json['password']
        cur = mysql.connection.cursor()
        #cur.execute("SELECT * from accounts  where username = '{0}'".format(username))
        cur.execute("SELECT * from accounts  where email = '{0}'".format(username))

        result = cur.fetchall()

        #if cur.rowcount == 1 and result[0][0] == username and result[0][2] == password:
        if sha256_crypt.verify(password, result[0][2]):
            session['user'] = request.json['username']

            #return redirect(url_for('home'))
            return render_template('home.html', logged_in=True,name=session['user'])

        return "log in failed"
    return app.send_static_file('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('Username:' + request.form['email'] + ' password' + request.form['password'])
        return 'Username:' + request.form['email'] + ' password' + request.form['password']

#lets you know which user session is active
@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'not logged in'

#clear out session
@app.route('/logout')
def logout():
   #remove username from session
   session.pop('user', None)
   return redirect(url_for('login'))

@app.route('/post/<id>', methods=['GET', 'POST'])
def post(id):
    if request.method == 'POST' and request.form['desc'] == '':
        cur = mysql.connection.cursor()
        cur.execute("update posts set views = views + 1 where id = '{0}'".format(id))
        mysql.connection.commit()

        cur.execute("select reply.email, reply.description, reply.time_posted, reply.reply_id, reply.parent_id from reply, posts where posts.id = reply.parent_id and posts.id = '{0}'".format(id))
        data = cur.fetchall()

        cur.execute("select * from posts where id = '{0}'".format(id))
        parent = cur.fetchall()
        cur.close()
        return render_template('post.html', logged_in=logged_in, data=data, parent=parent)

    if request.method == 'POST':
        #logic for post
        print(request.form['desc'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reply(email, time_posted, parent_id, description) VALUES(%s, now(), %s, %s)", (session['user'], id, request.form['desc']))
        mysql.connection.commit()
        cur.execute("update posts set replyc = replyc + 1 where id = '{0}'".format(id))
        mysql.connection.commit()
        cur.close()

    cur = mysql.connection.cursor()
    cur.execute("update posts set views = views + 1 where id = '{0}'".format(id))
    mysql.connection.commit()

    cur.execute("select reply.email, reply.description, reply.time_posted, reply.reply_id, reply.parent_id from reply, posts where posts.id = reply.parent_id and posts.id = '{0}'".format(id))
    data = cur.fetchall()

    cur.execute("select * from posts where id = '{0}'".format(id))
    parent = cur.fetchall()
    cur.close()

    if(data is None):
        return "404 error"

    return render_template('post.html', logged_in=logged_in, data=data, parent=parent)
'''
@app.route('/update.html', methods = ['GET','POST'])
def update():
    if request.method == 'POST':

        newusername = request.json['newusername']
        #newemail = request.json['newemail']
        #password = request.json['password']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE accounts SET username = %s WHERE username = %s",(newusername,session['user']))
        mysql.connection.commit()
        cur.close()
        return render_template('home.html', logged_in=True,name=newusername)


    if request.method == 'GET':
     return render_template('update.html',logged_in=True, name=session['user'])
'''

#@app.route('/')
#def index1():
#    posts = post.query.all()
#    return render_template('index.html',posts=posts)

@app.route('/search', methods=['GET', 'POST'])
def search():
    print("search route")
    print(request)
    if request.method == 'POST':
        dic = json.loads(request.data.decode())
        query = dic["query"]
        cur = mysql.connection.cursor()
        cur.execute("select * from posts where title like '%{0}%';".format(query))
        data_ = cur.fetchall()
        print(str(data_))
        mysql.connection.commit()
        return render_template('search.html', logged_in=logged_in,data=data_)

    return render_template('search.html', logged_in=logged_in)

@app.route('/searchprofile', methods=['GET', 'POST'])
def searchprofile():
    print("search route")
    print(request)
    if request.method == 'POST':
        dic = json.loads(request.data.decode())
        query = dic["query"]
        cur = mysql.connection.cursor()
        cur.execute("select * from posts where email like '%{0}%';".format(query))
        data_ = cur.fetchall()
        print(str(data_))
        mysql.connection.commit()
        return render_template('searchprofile.html', logged_in=logged_in,data=data_)

    return render_template('searchprofile.html', logged_in=logged_in)

@app.route('/results/<query>')
def results(query):
    cur = mysql.connection.cursor()
    cur.execute("select * from posts where title like '%{0}%';".format(query))
    data = cur.fetchall()
    print(str(data))
    mysql.connection.commit()
    #posts = post.query.whoosh_search(request.args.get('POST')).all()
    return render_template('results.html', logged_in=logged_in, data=data)

@app.route('/like', methods=['POST'])
def likes():
    dic = json.loads(request.data.decode())
    arr = dic["like_id"].split('/')
    id = arr[len(arr) - 1]
    cur = mysql.connection.cursor()
    cur.execute("update posts set likes = likes + 1 where id = {0}".format(id))
    mysql.connection.commit()
    return "done"