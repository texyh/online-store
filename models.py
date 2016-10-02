
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
        



'''
class School(db.Model):
    __tablename__ = 'school'
    id = db.Column('id',db.Integer,primary_key=True)
    school = db.Column('school',db.String,db.ForeignKey('profile.school'))

'''

