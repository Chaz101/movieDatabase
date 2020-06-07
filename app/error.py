from flask import render_template
from app import app, db
from . import main

@main.app_errorhandler(404)
def fourOhfour(error):
	return render_template('404.html'), 404

@main.app_errorhandler(500)
def fiveHundred(error):
	db.session.rollback()
	return render_template('500.html'), 500