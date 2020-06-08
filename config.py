import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' #get sec key from os (windows PC)
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') #get database uri from os, or use sqlite
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = os.environ.get('MAIL_SERVER') #server from os
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25) #server port
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['charlieconnor03@gmail.com'] #admin email
	MOVIE_API_BASE_URL ='https://api.themoviedb.org/3/movie/{}?api_key={}' #base url for api
	MOVIE_API_KEY = '859a79070480e0565c9326e50b3ec49e' #api key
