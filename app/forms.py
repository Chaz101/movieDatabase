from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from app.models import User
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()]) #Cant leave any form entry with DataRequired blank
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In') #submit field is button


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Regexp('^\w+$', message='Username can only contain letters and numbers.')]) #uname is alphanumeric
	email = StringField('Email', validators=[DataRequired(), Email()]) #must be a valid email adress (validators=[Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters.')]) #min 8 chars 
	password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')]) #must be EqualTo password
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Use a different username.') #usernames to be uniquew

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('That email is taken.') #emails unique


class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()]) #need to submit email so that password reset can be sent
	submit = SubmitField('Request Reset Password')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters.')]) #new password, matches above validators
	password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
	submit = SubmitField('Reset Password')


class ReviewForm(FlaskForm):
    title = StringField('Review title', validators=[DataRequired()]) #what is review called?
    review = TextAreaField('Movie review', validators=[DataRequired()]) #body of review
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Regexp('^\w+$', message='Username can only contain letters and numbers.')]) #edit username
	bio = TextAreaField('About me', validators=[Length(min=0, max=550)]) #edit bio, max 550 chars
	submit = SubmitField('Submit')

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username #ensure username isnt taken

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Use a different username.')


class EmptyForm(FlaskForm):
	submit = SubmitField('Submit')