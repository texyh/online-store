from flask_wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField, \
                    SelectField, RadioField
from wtforms.fields.html5 import DateField

from wtforms.validators import Required, Length, Email, EqualTo

from datetime import date





#Login form
class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])


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
    
    

#profile
class ProfileForm(Form):
    mychoice = [('ABU Zaria', 'ABU Zaria'), ('University of', 'Python'), ('text', 'Plain Text')]
    school = SelectField(
        'school',
        choices=mychoice,
        validators = [Required()]
    )


    phonenumber = TextField(
        'phonenumber',
        validators=[
            Length(min=11,max=14),
            Required()
        ]

    )

    gender = RadioField(
        'gender',
        choices = [('male','Male'),('female','Female')]

    )

    entrydate = DateField(
        'entrydate',
        format = '%d%m%Y'

    )
    
    graddate = DateField(
        'Pickdate',
        format = '%d%m%Y'

    )