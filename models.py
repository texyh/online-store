
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
#Flask bycrypt for password hashing    
from flask_bcrypt import Bcrypt

from flask_login import UserMixin

from views import app

from views import login_manager

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app

from cloudinary.utils import cloudinary_url




db =  SQLAlchemy(app)

app.config.from_object(os.environ.get('APP_SETTINGS'))


bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String, nullable=False,unique=True)
    email = db.Column('email', db.String, nullable=False,unique=True)
    password = db.Column('password',db.String,nullable=False)
    confirmed = db.Column('confirmed',db.Boolean,default=False)
    prof_rela = db.relationship('Profile',backref='user',lazy='dynamic')

    def __init__(self,username,email,password,confirmed):
        
        self.username = username    
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.confirmed = confirmed

    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True



    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))





        

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column('id',db.Integer,primary_key=True)
    phonenumber = db.Column('phonenumber',db.String,nullable=False)
    gender = db.Column('gender',db.String,nullable=False)
    entrydate = db.Column('entrydate',db.Date,nullable=False)
    graddate = db.Column('graddate',db.Date,nullable=False)
    school = db.Column('school',db.String,nullable=False)
    user_id = db.Column('user_id',db.Integer,db.ForeignKey('users.id'))

    def __init__(self,phonenumber,gender,
                entrydate,graddate,school,user_id):
        self.phonenumber = phonenumber
        self.gender = gender
        self.entrydate = entrydate
        self.graddate = graddate
        self.school = school
        self.user_id = user_id
        

#class UserProfile(db.Model):


'''
class School(db.Model):
    __tablename__ = 'school'
    id = db.Column('id',db.Integer,primary_key=True)
    school = db.Column('school',db.String,db.ForeignKey('profile.school'))

'''


class Market(db.Model):
    __tablename__ = 'market'

    id = db.Column('id',db.Integer,primary_key=True)
    itemname = db.Column('itemname',db.String,nullable=False)
    description = db.Column('description',db.String,nullable=False)
    price = db.Column('price',db.String,nullable=True)
    itemtype = db.Column('itemtype',db.String)
    free = db.Column('free',db.Boolean,default=False)
    imagename = db.Column('imagename',db.String)
    school = db.Column('school',db.String)
    seller = db.Column('seller',db.String)

    def __init__(self,itemname,description,price,itemtype,free,imagename,school,seller):

        self.itemname = itemname
        self.description = description
        self.price =  price
        self.itemtype = itemtype
        self.free = free
        self.imagename = imagename
        self.school = school
        self.seller = seller

    def image_url(self):
        result = cloudinary_url(self.imagename, width=200, height=200)
        return result[0]

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column('id',db.Integer,primary_key=True)
    eventtitle= db.Column('eventtitle',db.String,nullable=False)
    description = db.Column('description',db.String,nullable=False)
    price = db.Column('price',db.String)
    eventtype = db.Column('eventtype',db.String,nullable=True,default="")
    date = db.Column('date',db.Date,nullable=False)
    time = db.Column('time',db.Time,nullable=False)
    eventvenue = db.Column('eventvenue',db.String,nullable=False)
    eventoption = db.Column('eventoption',db.Boolean,default=False)
    eventschool = db.Column('school',db.String)
    free = db.Column('free',db.Boolean,default=False)
    imagename = db.Column('imagename',db.String)
    eventposter  = db.Column('Eventposter',db.String)
    def __init__(self,eventtitle,description,price,eventtype,date,time,eventvenue, \
                 eventoption,eventschool,free,imagename,eventposter):

        self.eventtitle = eventtitle
        self.description = description
        self.price =  price
        self.eventtype = eventtype
        self.date = date
        self.time =time
        self.eventvenue = eventvenue
        self.eventoption = eventoption
        self.eventschool = eventschool
        self.free = free
        self.imagename = imagename
        self.eventposter  = eventposter 

    def image_url(self):
        result = cloudinary_url(self.imagename, width=200, height=200)
        return result[0]




class Pulse(db.Model):
    __tablename__ ='pulse'

    id = db.Column('id',db.Integer,primary_key=True)
    post = db.Column('post',db.String)
    school = db.Column('school',db.String)
    poster = db.Column('poster',db.String)
    likes = db.Column('likes',db.Integer)


    def __init__(self,post,school,poster):
        self.post = post
        self.school = school
        self.poster = poster
        self.likes = likes

    def likes(self):
        return self.likes




class PostComment(db.Model):
    __tablename__ = 'postcomment'
    id = db.Column('id',db.Integer,primary_key=True)
    comment = db.Column('comment',db.String)
    commentor = db.Column('commentor',db.String)
    pulseonwer = db.Column('pulseonwer',db.Integer)

    def __init__(self,comment,commentor):
        self.comment = comment
        self.commentor = commentor
        self.pulseonwer = pulseonwer



class PulseLikes(db.Model):
    __tablename__ = "pulselikes"
    id = db.Column('id',db.Integer,primary_key=True)
    pulseonwer = db.Column('pulseonwer',db.Integer)
    likers = db.Column('likers',db.String)
    

    def __init__(self,pulseonwer,likers,likes):
        self.pulseonwer = pulseonwer
        self.likers = likers
        


