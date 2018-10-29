from flask import Flask, request, redirect, render_template
import os
import cgi
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True  

def is_valid(data):
    if len(data) > 2 and len(data) < 21:
        return True
    else:
        return False

def is_verified(password_arg, verify_arg):
    if password_arg == verify_arg:
        return True
    else:
        return False

@app.route("/")
def index():
    template = jinja_env.get_template('hello_user.html')
    return template.render()

@app.route('/', methods=['POST'])
def validate_data():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''
    
#check username
    if not is_valid(username):
        username_error = "That's not a valid username"
        username = ''

    else:
        if len(username) < 0:
            username_error = "That's not a valid username"
            username = ''

    if not is_valid(password):
        password_error = "That's not a valid password"
    else:
        if len(password) < 0:
            password_error = "That's not a valid password"

    if not is_verified(password, verify):
        verify_error = "Passwords don't match"
    else:
        if len(password) < 1:
            verify_error = "Passwords don't match"

    password = ''
    verify = ''
    email = ''

    if not username_error and not password_error and not verify_error:
        return redirect('/welcome?username={0}'.format(username))

    else:
        template = jinja_env.get_template('hello_user.html')
        return template.render(username_error=username_error,
            password_error=password_error,
            verify_error=verify_error,
            username=username,
            password=password, 
            verify=verify)
    

@app.route("/welcome")
def welcome():
    username = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)

app.run()
