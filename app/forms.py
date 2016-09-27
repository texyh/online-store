from flask_wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField, \
                    SelectField, RadioField, BooleanField, ValidationError, \
                    TextAreaField
from wtforms.fields.html5 import DateField, TimeField

from flask_wtf.file import FileField

from wtforms.validators import Required, Length, Email, EqualTo

from datetime import date

from models import *



#Login form
class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField("keep me logged in")


    


#signup form
class RegistrationForm(Form):
    username = TextField(
        'username',
        validators=[Required(),Length(min=3, max=25)]
    )
    email = TextField(
        'email',
        validators=[Required(),  Email(message="enter your email"), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[Required('minimum of 6 characters'), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        're-Password',
        validators=[
            Required(), EqualTo('password', message='Password must match.')
        ]
    )

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registration')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username already taken')


    
    

#profile
class ProfileForm(Form):
    mychoice = [('ABU Zaria', 'ABU Zaria'), ('UniLag', 'UniLag'), ('UniAbuja', 'UniAbuja')]
    school = SelectField(
        'school',
        choices=mychoice,
        validators = [Required('choose a school')]
    )


    phonenumber = TextField(
        'phonenumber',
        validators=[
            Length(min=11,max=14),
            Required('min of 11 characters')
        ]

    )
  
    gender = RadioField(
        'gender',
        choices = [('male','Male'),('female','Female')]

    )


    entry = DateField(
        'entry',
        format='%Y-%m-%d'

    )
    
    grad = DateField(
        'Pick',
        format = '%Y-%m-%d'

    )



class MarketForm(Form):
    mychoice = [('trade','Trade'),('rent','Rent'),('sale','Sale')]
    item_image = FileField('item_photo')
    item_name = TextField('itemname',validators=[Required()])
    description = TextField('Description',validators = [Required()])
    market_option = RadioField('free',choices=[('free','free')],validators= [Required()])
    market_type = SelectField('SelectType',choices=mychoice,validators=[Required()])



class PulseForm(Form):
    staus = TextAreaField("whats on your mind",validators=[Required()])
    status_image = FileField('Add Photo')



class EventForm(Form):
    mychoice = [('tgif','TGIF'),('religious','Religious'),('academic','Academic')]
    eventimage = FileField('Add Photo')
    eventtitle = TextField('Event Title',validators=[Required()])
    description = TextField('Description',validators = [Required()])
    eventdat = DateField('Event Date',format='%Y-%m-%d')
    eventtime = TimeField('Event Time',)
    eventvenue = TextField('Event Venue',validators=[Required()])
    eventoption = RadioField('free',choices=[('free','free')],validators= [Required()])
    eventtype = SelectField('SelectType',choices=mychoice,validators=[Required()])

