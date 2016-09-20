from flask import Flask, render_template, request, url_for, redirect, \
				flash
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS'))


from forms import *


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html',form=form)

    

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST' and form.validate():
		return 'yaay'
	return render_template('index.html',form=form)


@app.route('/registration', methods = ['GET','POST'])
def registration():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		return redirect(url_for('profile'))
	return render_template('registration.html',form=form)


@app.route('/profile', methods = ['GET','POST'])
def profile():
	form = ProfileForm(request.form)
	if request.method == 'POST' and form.validate():
		return 'yayy'
		return redirectj(url_for('login'))
	return render_template('profile.html',form=form)


@app.route('/confirmation')
def confirmation():
	return render_template ('confirmation.html')


