from flask import Flask, render_template, redirect, request, flash, session
from mysqlconnection import MySQLConnector
import re
import md5
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'hellothere12345'
mysql = MySQLConnector(app, 'login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['post'])
def create():
    count = 0
    if len(request.form['first_name']) < 1:
        flash("First Name cannot be empty")
        count += 1
    if len(request.form['last_name']) < 1:
        flash("Last Name cannot be empty")
        count += 1
    if len(request.form['email']) < 1:
        flash("email must be entered")
        count+= 1
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        count+=1
    if len(request.form['password']) < 6:
        flash("Weak password")
        count+=1
    if len(request.form['password']) != len(request.form['conf_password']):
        flash("Password does Not Match")
        count+= 1
    # if len(request.form['email']) == user.email:
    #     flash("opps!, email already exist!")
    if count < 1:
        password = md5.new(request.form['password']).hexdigest();
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES(:first_name, :last_name, :email, :password, NOW(), NOW())"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': password
        }
        mysql.query_db(query, data)
        return redirect('/success')
    else:
        return redirect('/')
@app.route('/success')
def success():
    query = "SELECT users.id, users.first_name, users.last_name, users.email, users.created_at FROM users"
    user = mysql.query_db(query)
    return render_template('success.html', all_user=user)

@app.route('/login', methods=['post'])
def login():
    password = md5.new(request.form['password']).hexdigest()
    email = request.form['email']
    query = "SELECT * FROM users where users.email = :email AND users.password = :password"
    data = { 'email': email, 'password': password}
    user = mysql.query_db(query,data)
    return redirect('/success')
app.run(debug=True)
