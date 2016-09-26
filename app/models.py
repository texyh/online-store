
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db =  SQLAlchemy(app)

app.config.from_object(os.getenv('APP_SETTINGS'))


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
    prof_rela = db.relationship('Profile',backref='users',lazy='dynamic')

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





        


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column('id',db.Integer,primary_key=True)
    phonenumber = db.Column('phonenumber',db.String,nullable=False)
    gender = db.Column('gender',db.String,nullable=False)
    entrydate = db.Column('entrydate',db.DateTime,nullable=False)
    graddate = db.Column('graddate',db.DateTime,nullable=False)
    school = db.Column('school',db.String,nullable=False)
    user_id = db.Column('user_id',db.Integer,db.ForeignKey('users.id'))
    schoolr = db.relationship('School',backref='profile',lazy='dynamic')

    def __init__(self,phonenumber,gender,
                entrydate,graddate,school,user_id):
        self.phonenumber = phonenumber
        self.gender = gender
        self.entrydate = entrydate
        self.graddate = graddate
        self.school = school
        self.user_id = user_id
        




class School(db.Model):
    __tablename__ = 'school'
    id = db.Column('id',db.Integer,primary_key=True)
    school = db.Column('school',db.String,db.ForeignKey('profile.school'))





class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column('id',db.Integer,primary_key=True)
    itemname = db.Column('itemname',db.String,nullable=False)
    description = db.Column('description',db.String,nullable=False)
    price = db.Column('price',db.String,nullable=False)
    itemtype = db.Column('itemtype',db.String,nullable=False)
    date = db.Column('date',db.DateTime,nullable=False)
    time = db.Column('time',db.DateTime,nullable=False)

    def __init__(self,itemname,description,price,itemtype,date,time):

        self.itemname = itemname
        self.description = description
        self.itemtype = itemtype
        self.date = date
        self.time =time








db.create_all()





