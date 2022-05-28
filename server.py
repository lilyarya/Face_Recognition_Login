from flask import Flask, render_template, request, url_for, redirect, Blueprint, send_from_directory
#global request object to access incoming request data that will be submitted via the HTML form you built in the last step.
#url_for Generates a URL to the given endpoint with the method provided.
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from login import login_check as lc
from register import register_on_submit as rs

main = Blueprint('main', __name__)
#A blueprint is an object that allows 
# defining application functions without requiring an application object ahead of time

secret_key = str(os.urandom(24))

app = Flask(__name__)
app.config['TESTING'] = False
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'deployment'
app.config['SECRET_KEY'] = secret_key

app.register_blueprint(main)

class LoginForm(FlaskForm):
    email = StringField('Enter user ID', validators=[DataRequired()])
    url = StringField('DataURL', validators=[])
    submit = SubmitField('LOGIN')

class RegisterForm(FlaskForm):
    email = StringField('Enter user ID', validators=[DataRequired()])
    url = StringField('DataURL', validators=[])
    submit = SubmitField('REGISTER')

email = None
url = None

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html') 
    # render_template() function, which indicates to Flask that the route should display an HTML template

@app.route('/login', methods=['GET', 'POST'])
# tuple ('GET', 'POST') to accept both GET and POST requests. GET and POST are HTTP methods.
#By default, only GET requests are accepted, which are used to retrieve data
def login():
    global email, url
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        url = form.url.data
        return redirect(url_for('.login_submit'))
    elif request.method == 'POST': 
        #POST requests are used to submit data to a specific route, which often changes the data on the server
        form.email.data = email
        form.url.data = url
    return render_template('index.html', form=form)

@app.route('/login_submit')
def login_submit():  
    global email, url
    if email == '' or url == '':
        return redirect(url_for('.login'))
    if email == None or url == None:
        return redirect(url_for('.login'))

    status = lc(email, url) #gettin status from login_check from login.py file and comparing it

    if status == "Image not clear ! Please try again !" or status == "Data does not exist !" or status == "This user ID is not registered yet" or status == "No face detected" or status == "Multiple faces detected":
        return render_template('fail.html', msg=status) #if failed, render fail html page
    elif status == "Successfully Logged in":
        app.logger.info("Login Success")
        return render_template('success.html', msg=status) #if successful ,render success html page
    else:
        app.logger.info("Login Fail")
        return render_template('fail.html', msg=status)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global email, url
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        url = form.url.data
        return redirect(url_for('.register_submit'))
    elif request.method == 'POST':
        form.email.data = email
        form.url.data = url
    return render_template('register.html', form=form)

@app.route('/register_submit')
def register_submit():
    global email, url
    if email == '' or url == '':
        return redirect(url_for('.register'))
    if email == None or url == None:
        return redirect(url_for('.register_submit'))

    status = rs(email, url) #gettin status from register_on_submit  from regiter.py file

    if status == "This user ID is already registered" or status == "No face detected" or status == "Multiple faces detected":
       return render_template('fail.html', msg=status)
    elif status == "Registration Successful":
        app.logger.info("Registration Success")
        return render_template('success.html', msg=status)
    else:
        app.logger.info("Registration fail")
        return render_template('fail.html', msg=status)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
 #send_from_directory =Send a file from a given directory with send_file. 
 # This is a secure way to quickly expose static files from an upload folder or something similar.
if __name__ == "__main__":
    app.run(debug=True)