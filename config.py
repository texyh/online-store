import os
basedir = os.path.abspath(os.path.dirname(__file__)) 

#Base config 

class Config(object):
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


	
class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'development.sqlite')


	

class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


