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
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _1('Please login to access this page.')
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
photos = UploadSet('photos', IMAGES)

if not app.debug:
	if app.config['MAIL_SERVER']:
		auth = None
		if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
			auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
		secure = None
		if app.config['MAIL_USE_TLS']:
			secure = ()
		mail_handler = SMTPHandler(
			mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
			fromaddr='noreply@' + app.config['MAIL_SERVER'],
			toaddr=app.config['ADMINS'], subject='Database Failed',
			credentials=auth, secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)

	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/movie.log', maxBytes=10240, backupCount=10)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineo)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.setLevel(logging.INFO)
	app.logger.info('Movie startup')

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/authenticate')
	app.config.from_object(Config[config_name])
	configure_uploads(app,photos)
	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .request import configure_request
	configure_request(app)
	mail.init_app(app)

from app import routes, models, errors
