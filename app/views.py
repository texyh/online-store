from flask import Flask, render_template, request, url_for, redirect, \
				flash, session
import os
from flask_sqlalchemy import SQLAlchemy



from flask_login import LoginManager
from flask_login import login_required, logout_user

app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS'))

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '/login'




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
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next')) or 'yaay'
		
		flash('invalid login details')
	return render_template('index.html',form=form)




@app.route('/registration', methods = ['GET','POST'])
def registration():
	form = RegistrationForm()
	if request.method == 'POST': 
		if form.validate():
			email = form.email.data
			username = form.username.data
			password = form.password
			user = User(username=username,
						email=email,password=password,confirmed=False)

			db.session.add(user)
			db.session.commit()
			token =  user.generate_confirmation_token()

			return redirect(url_for('profile'))
		flash('username or email already exist')
	return render_template('registration.html',form=form)



@app.route('/profile', methods = ['GET','POST'])
def profile():
	form = ProfileForm()
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


