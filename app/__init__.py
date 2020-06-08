import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import Config

app = Flask(__name__) #start Flask
app.config.from_object(Config) #define config.py as app.config
db = SQLAlchemy(app) #user SQLAlchemy as db
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = ('Please login to access this page.')
mail = Mail(app)
bootstrap = Bootstrap(app) #start Bootstrap (styling)
moment = Moment(app)

def create_app(config_name): #starts app
	if not app.debug:
		if app.config['MAIL_SERVER']: #check for server host
			auth = None
			if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']: #check is user/pw for host needed
				auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
			secure = None
			if app.config['MAIL_USE_TLS']:
				secure = ()
			mail_handler = SMTPHandler(
				mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
				fromaddr='noreply@' + app.config['MAIL_SERVER'], #if db fails send email from noreply@ (mail server defined in config)
				toaddr=app.config['ADMINS'], subject='Database Failed', #to the admins defined in config
				credentials=auth, secure=secure)
			mail_handler.setLevel(logging.ERROR)
			app.logger.addHandler(mail_handler)

		if not os.path.exists('logs'): #create logs file if one not made
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/movie.log', maxBytes=10240, backupCount=10) #create a site log
		file_handler.setFormatter(logging.Formatter(
			'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineo)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)
		app.logger.setLevel(logging.INFO)
		app.logger.info('Movie startup')

		from .request import configure_request
		configure_request(app)
		mail.init_app(app)

from app import routes, models, error
