from flask import Flask, render_template, flash, redirect, session, request, jsonify, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, PasswordField, SubmitField, IntegerField,BooleanField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
# from bs4 import BeautifulSoup
import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash





class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    loginButton = SubmitField(label='Login')

class SignUpForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    checkBox = BooleanField(default=False)
    password = PasswordField(label='Password', validators=[DataRequired()])
    signUpButton = SubmitField(label='Sign Up')

class adminForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    loginButton = SubmitField(label='Login')


    
# Variables
app  = Flask(__name__)
app.secret_key = "beautifulsoup"


# Database connection function
def connect_db():
    conn = sqlite3.connect('users.db')
    return conn

# Create user table if it doesn't exist
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                       (email TEXT PRIMARY KEY, password TEXT NOT NULL)''')
    conn.commit()
    conn.close()


# # Database admin connection function
# def connect_db():
#     adminConn = sqlite3.connect('users.db')
#     return adminConn

# # Create admin table if it doesn't exist
# def init_db():
#     adminConn = connect_db()
#     cursor = adminConn.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                        (email TEXT PRIMARY KEY, password TEXT NOT NULL)''')
#     adminConn.commit()
#     adminConn.close()


# Routes


@app.route('/', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm()
    login_form = LoginForm()

    if signup_form.validate_on_submit():
        conn = connect_db()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute('SELECT * FROM users WHERE email = ?', (signup_form.email.data,))
        user = cursor.fetchone()

        if user is not None:
            message = 'Email already exists. Please choose a different one.'
            return render_template('sign-up.html', form=signup_form, errormessage=message)

        # Hash password before storing (implement password hashing with bcrypt or similar)
        # hashed_password = 'implement_password_hashing(signup_form.password.data)'  # Replace with actual hashing logic

        # Insert user data into database
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                       (signup_form.email.data, signup_form.password.data))
        conn.commit()
        conn.close()
        print("successful")
        flash('Registration successful! You can now log in.')


        return render_template('login.html', form=login_form)


    else:
        print("e no work")
    return render_template('sign-up.html', form=signup_form)





# ... (rest of your code)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (login_form.email.data,))
        user = cursor.fetchone()

        if user:
            # Check password using hashed password           
            if user[1] == login_form.password.data or user[2] == login_form.password.data or user[3] == login_form.password.data:
                print('Login successful!')
                return render_template('home.html')
            else:
                message = "Incorrect password"
                print('Incorrect password')
                return render_template('login.html', form=login_form, errormessage=message )
        else:
            print('Account doesn\'t exist')
            message = "Account doesn't exist"
            return render_template('login.html', form=login_form, errormessage=message )


        conn.close()

    return render_template('login.html', form=login_form)


@app.route('/home')
def home():
 
    return render_template("home.html")

@app.route('/about')
def about():
 
    return render_template("about.html")

@app.route('/contact')
def contact():
 
    return render_template("contact.html")

@app.route('/layout')
def layout():
 
    return render_template("layout.html")

@app.route('/admin')
def admin():
 
    return render_template("admin.html")


@app.route('/adminsignin', methods=['GET', 'POST'])
def adminsignin():
    admin_form = adminForm()

    if admin_form.validate_on_submit():
    
            # Check password using hashed password           
        if admin_form.email.data == 'admin@autocar.com' and admin_form.password.data == 'admin123':
            print('Login successful!')
            message = "Login successful"
            return render_template('admin.html', form=admin_form, message="Login successful")
        else:
            message = "Wrong Email or Password You are not an admin"
            print('Incorrect password')
            return render_template('adminsignin.html', form=admin_form, errormessage=message )


    return render_template('adminsignin.html', form=admin_form)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)