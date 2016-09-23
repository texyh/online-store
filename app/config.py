import os
basedir = os.path.abspath(os.path.dirname(__file__))
 

#Base config 

class Config(object):
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

	# mail settings
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True


	# gmail authentication
	MAIL_USERNAME = os.getenv('MAIL_USERNAME')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

	# mail accounts
	MAIL_DEFAULT_SENDER = 'onetwotechdemo@gmail.com'


	
class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'deve.sqlite')


	

class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


