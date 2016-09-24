from flask_mail import Mail, Message 
from flask import render_template
from views import app

mail = Mail(app)

def send_mail(to,subject,template,):
	msg = Message(subject,recipients=[to],html=template,
				sender=app.config['MAIL_DEFAULT_SENDER'])
	


	with app.app_context():
		mail.send(msg)

