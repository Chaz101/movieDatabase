from flask import render_template
from app import app, db

@app.errorhandler(404)
def fourOhfour(error):
	return render_template('404.html'), 404 #in 404 error, display 404.html

@app.errorhandler(500)
def fiveHundred(error):
	db.session.rollback()
	return render_template('500.html'), 500 #in 500 error, diplaty 500.html