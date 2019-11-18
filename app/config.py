import os, sys

def check_redispw():
	if not os.getenv("REDIS_PW"):
		return 'redis://localhost:6379/0'
	else:
		return 'redis://:{pw}@redis:6379/0'.format(pw=os.getenv('REDIS_PW'))

def check_db():
	if not os.getenv("POSTGRES_USER") and not os.getenv("POSTGRES_PW") and not os.getenv("POSTGRES_URL"):
		return "postgresql+psycopg2://localhost:5432/app"
	else:
		return 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=DATABASE)

class Config(object):
	DEBUG = False
	CSRF_ENABLED = True
	SECRET_KEY = "63706bcd61528a3cee6826fbf8ce51c4"
	JWT_SECRET_KEY = "a6603d87a7b2bdf957861323d7131c44"
	JWT_BLACKLIST_ENABLED = True
	JWT_BLACLIST_TOKEN_CHECKS = ['access', 'refresh']
	REDIS_URL = check_redispw()
	#BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
	DATABASE_PATH = os.path.join(os.getenv("HOME"), "app.db")
	SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DATABASE_PATH)

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	


class DevelopmentConfig(Config):
	"""Config for dev"""
	DEBUG = True

class TestingConfig(Config):
	"""Config for testing """

	DEBUG = True
	TESTING = True

	#TODO: change database to testing

class StageingConfig(Config):
	"""Config for stageing"""

	DEBUG = True

class ProductionConfig(Config):
	"""Config for production """

	DEBUG = False
	TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StageingConfig,
    'production': ProductionConfig
}