from flask_mail import Mail, Message
from flask import render_template
from views import app

from decorators import async

mail = Mail(app)




@async
def send_async_mail(app,msg):

	with app.app_context():
		mail.send(msg)





def send_mail(to,subject,template,):
	msg = Message(subject,recipients=[to],html=template,
				sender=app.config['MAIL_DEFAULT_SENDER'])

	send_async_mail(app,msg)



