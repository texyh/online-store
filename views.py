from flask import Flask, render_template, request, url_for, redirect, \
                flash, session, send_from_directory
import os
from flask_sqlalchemy import SQLAlchemy

import time


from flask_login import LoginManager, UserMixin
from flask_login import login_required, logout_user, login_user, current_user

from werkzeug.utils import secure_filename

from flask_dropbox import Dropbox


app = Flask(__name__)

app.config.from_object(os.environ.get('APP_SETTINGS'))

#flask-login
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '/login'

#flask-dropbox
dropbox = Dropbox(app)

#cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url



from forms import *
from models import *
#from models import User, Profile, db, bcrypt
from emails import send_mail
from decorators import check_confirmed

photos = UploadSet('photos', IMAGES)


configure_uploads(app, photos)



@app.route('/')
@login_required
def index():
    return redirect(url_for('home',username=current_user.username))

   


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    rform = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username =  form.username.data
        password = form.password.data
        user_exist = User.query.filter_by(username=username).first()
        if user_exist is not None and bcrypt.check_password_hash(user_exist.password,\
                password) == True:
            login_user(user_exist,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('home', \
                username=current_user.username)) 
        
        flash('invalid login details')
    return render_template('index.html',form=form,rform=rform)




@app.route('/registration', methods = ['POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST': 
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = User(username=username,
                        email=email,password=password,confirmed=False)

            db.session.add(user)
            db.session.commit()
            token =  user.generate_confirmation_token()
            confirm_url = url_for('confirm_email',token=token,_external=True)
            html = render_template('email/email.html',user=user,confirm_url=confirm_url)
            subject = "confirm your account"
            send_mail(user.email,subject,html)
            session['username'] = username
            return redirect(url_for('profile'))
        flash('username or email already exist')
        return redirect(url_for('login'))
    #return render_template('registration.html',form=form)




@app.route('/home/<username>',methods=['GET','POST'])
@login_required
@check_confirmed
def home(username):
    form = MarketForm()
    form.markettype.choices = [(None,'Option'),('trade','Trade'),\
                            ('rent','Rent'),('sale','Sale')]
    user_school = Profile.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        if form.validate():
            itemname = form.itemname.data
            itemdescription = form.description.data
            markettype = form.markettype.data
            price = form.price.data
            #ptime = time.time()
            up_file = form.itemimage.data
            #filename = secure_filename(form.itemimage.data.filename)
            #filename = str(ptime)+filename
            #client = dropbox.client
            if form.price.data:
                #form.itemimage.data.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'],\
                 #filename))
                # Actual uploading process
                #result = client.put_file('/ipreneur_uploads' + filename, file_obj.read())
                upload_result = upload(up_file)
                imagename=upload_result['public_id']
                market = Market(itemname=itemname,description=itemdescription,itemtype=markettype,\
                    price=price,free=False,imagename=imagename,school=user_school.school)
                db.session.add(market)
                db.session.commit()
                return redirect(url_for('home',username=current_user.username))
                
            else:
                #form.itemimage.data.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'],\
                #filename))
                upload_result = upload(up_file)
                imagename=upload_result['public_id']
                market = Market(itemname=itemname,description=itemdescription,itemtype=markettype,\
                    price=None,free=True,imagename=imagename,school=user_school.school)
                db.session.add(market)
                db.session.commit()
                return redirect(url_for('home',username=current_user.username))

        flash('Enter all fields')
        return redirect(url_for('home',username=current_user.username))
    market = Market.query.filter_by(school=user_school.school).all()
    return render_template('home.html',form=form,market=market)





@app.route('/profile', methods = ['GET','POST'])
def profile():
    form = ProfileForm()
    form.school.choices = [(None,'Select School'),('ABU Zaria', 'ABU Zaria'), \
                        ('UniLag', 'UniLag'), ('UniAbuja', 'UniAbuja')]
    form.gender.choices = [('male','Male'),('female','Female')]
    if request.method == 'POST':
        user = User.query.filter_by(username=session['username']).first()
        if form.validate():
            school=form.school.data
            phonenumber=form.phonenumber.data
            entry=form.entry.data
            grad = form.grad.data
            gender = form.gender.data
            profile = Profile(phonenumber=phonenumber,gender=gender,\
                    entrydate=entry,graddate=grad,school=school,user_id=user.id)
            db.session.add(profile)
            db.session.commit()
            login_user(user)
            return redirect(url_for('unconfirmed',username=user.username))
        return 'bad form'
    return render_template('profile.html',form=form)




@app.route('/confirm_email/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash('Your Account has Already been confirmed')
        return redirect(url_for('home',username=current_user.username))
    if current_user.confirm(token):
        flash('Thank you for confirmation, Welcome on board')
        return redirect(url_for('home',username=current_user.username))
    else:
        flash('The Token you supplied is bad or has expired')
        return redirect(url_for('resend'))




@app.route('/unconfirmed/<username>',methods=['GET'])
@login_required
def unconfirmed(username):
    if current_user.confirmed:
        return redirect(url_for('home',username=current_user.username))
    return render_template('unconfirmed.html')




@app.route('/resend')
@login_required
def resend():
    token = current_user.generate_confirmation_token()
    confirm_url = url_for('confirm_email',token=token,_external=True)
    html = render_template('email/email.html',user=current_user,confirm_url=confirm_url)
    subject = "confirm your account"
    send_mail(current_user.email,subject,html)
    flash('another link has been sent','success')
    return redirect(url_for('unconfirmed',username=current_user.username))




@app.route('/event/<username>', methods=['GET','POST'])
@login_required
@check_confirmed
def event(username):
    form = EventForm()
    if request.method == 'POST':
        if form.validate():
            return 'this page is still under construction'
        flash('Enter all fields')
        return redirect(url_for('event',username=current_user.username))
    return render_template('event.html',form=form)




@app.route('/pulse/<username>', methods=['GET','POST'])
@login_required
@check_confirmed
def pulse(username):
    form = PulseForm()
    if request.method == 'POST':
        return form.status.data

    return render_template('pulse.html',form=form)
'''
@app.route('/uploaded/<filename>')
def uploaded(filename):
    return cloudinary_url(filename, width=200, height=200)
    #return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)
'''


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('login'))