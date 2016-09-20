
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
#Flask bycrypt for password hashing    
from flask_bcrypt import Bcrypt





from views import app

db =  SQLAlchemy(app)

app.config.from_object(os.getenv('APP_SETTINGS'))


bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('firstname', db.String, nullable=False,unique=True)
    email = db.Column('email', db.String, nullable=False,unique=True)
    password = db.Column('password',db.String,nullable=False)
    phonenumber = db.Column('phonenumber',db.String,nullable=False)
    gender = db.Column('gender',db.String,nullable=False)
    entrydate = db.Column('entrydate'db.DateTime,nullable=False)
    graddate = db.Column('graddate',db.DateTime,nullable=False)
    confirmed = db.Column('confirmed',db.Boolean,nullable=False,default=False)
    school = db.Column('school',db.String,nullable=False)
    schoolr = db.Relationship('School',backref='users',lazy='dynamic')


    def __init__(self,username,email,password,phonenumber,gender,\
    			entrydate,gradedate,confirmed,school):
    	
    	self.username = username	
    	self.email = email
    	self.password = 
    	self.phonenumber = phonenumber
    	self.gender = gender
    	self.entrydate = entrydate
    	self.gradedate = graddate
    	self.confirmed = confirmed



class School(db.Model):
	__tablename__ = 'school'
	id = db.Column('id',db.Integer,primary_key=True)
	school = ('school'db.String,db.ForeignKey('users.school'))

	def __init__(self,school):
		self.school = school




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



class Event(db.Model):
	__tablename__ = 'event'










