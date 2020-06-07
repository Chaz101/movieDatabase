from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Review
from app.email import send_password_reset_email
from app.request import get_movies, get_movie, search_movie

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.locale = str(get_locale())

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	popular_movies = get_movies('popular')
	upcoming_movie = get_movies('upcoming')
	now_showing_movie = get_movies('now_playing')
	title = 'Home - Movie Database'
	search_movie = request.args.get('movie_query')

	if search_movie:
		return redirect(url_for('main.search', movie_name=search_movie))
	else:
		return render_template('index.html', title=title, popular=popular_movies, upcoming=upcoming_movie, now_playing=now_showing_movie)


@app.route('/search/<movie_name>')
def search(movie_name):
	movie_name_list = movie_name.split(" ")
	movie_name_format = '+'.join(movie_name_list)
	searched_movies = search_movie(movie_name_format)
	title = f'search results for {movie_name}'
	return render_template('search.html', movies=searched_movies)


@app.route('/movie/review/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_review(id):
	form = ReviewForm()
	movie = get_movie(id)
	if form.validate_on_submit():
		title = form.title.data
		review = form.review.data
		new_review = Review(movie_id=movie_id, movie_title=title, image_path=movie.poster, movie_review=review, user=current_user)
		new_review.save_review()
		return redirect(url_for('.movie', id=movie.id))

	title = f'{movie.title} review'
	return render_template('new_review.html', title=title, review_form=form, movie=movie)


@app.route('/movie/<int:id>')
def movie(id):
    movie = get_movie(id)
    title = f'{movie.title}'
    reviews = Review.get_reviews(movie.id)

    return render_template('movie.html', title=title, movie=movie, reviews=reviews)


@app.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	if user is None:
		abort(404)
	return render_template('user.html', user=user)	


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.bio = form.bio.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.bio.data = current_user.bio
	return render_template('edit_profile.html', title='Edit Profile', form=form)