from flask_mail import Message
from flask import render_template
from app import app, mail
from threading import Thread

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body): #order items
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
	token = user.get_reset_password_token()
	send_email(_('[Watchlist] Reset Your Password'), #subject of msg
				sender=app.config['ADMINS'][0], #sender email is 'ADMINS' in config.py
				recipients=[user.email], #registered user enail
				text_body=render_template('email/reset_password.txt', user=user, token=token), #send reset pw msg in both plaintext and html
				html_body=render_template('email/reset_password.html', user=user, token=token))