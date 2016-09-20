from flask import Flask, render_template, request, url_for, redirect, \
				flash, session
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS'))


from forms import *

from models import *


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html',form=form)

   


@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST' and form.validate():
		username =  form.username.data
		password = form.password.data
		user_exist = User.query.filter_by(username=username).first()
		if user_exist is not None and bcrypt.check_password_hash(user_exist.password,\
		 		password) == True:
			return 'yayy'
		else:
			flash('invalid login details')
			return redirect(url_for('login'))
	return render_template('index.html',form=form)




@app.route('/registration', methods = ['GET','POST'])
def registration():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		email = form.email.data
		username = form.username.data
		password = form.password
		email_exist = User.query.filter_by(email=email).first()
		username_exist = User.query.filter_by(username=username).first()
		if email_exist is None and username_exist is None:
			try:
				user = User(username=username,
							email=email,password=password)

				db.session.add(user)
				db.session.commit()
				return redirect(url_for('profile'))
			except:
				db.session.rollback()
		flash('username or email already exist')
		return redirect(url_for('registration'))
	return render_template('registration.html',form=form)


@app.route('/profile', methods = ['GET','POST'])
def profile():
	form = ProfileForm(request.form)
	form.school.choices = [('ABU Zaria', 'ABU Zaria'),
						 ('University of', 'Python'), ('text', 'Plain Text')]
	form.gender.choices = [('male','Male'),('female','Female')]
	if request.method == 'POST':
		if form.validate():
			return form.graddate.data 
		return 'bad form'
	return render_template('profile.html',form=form)


@app.route('/confirmation')
def confirmation():
	return render_template ('confirmation.html')


