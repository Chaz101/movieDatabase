import urllib.request, json
from .models import Movie

#api key for themoviedb (where movies are stored)
api_key = '859a79070480e0565c9326e50b3ec49e'
#api for webisite
base_url = 'https://api.themoviedb.org/3/movie/{}?api_key={}'

#fetches key & base url from config.py
def configure_request(app):
	global api_key, base_url
	api_key = app.config['MOVIE_API_KEY']
	base_url = app.config['MOVIE_API_BASE_URL']

#gets groups of movies by importing category and api key into the 2 open spaces of base_url
def get_movies(category):
	get_movies_url = base_url.format(category, api_key)
	with urllib.request.urlopen(get_movies_url) as url:
		get_movies_data = url.read()
		get_movies_response = json.loads(get_movies_data)

		movie_results = None

		if get_movies_response['results']:
			movie_results_list = get_movies_response['results']
			movie_results = process_results(movie_results_list)
	return movie_results

#gets specific movies in same way as above but swaps category with specific movie ID
def get_movie(id):
	get_movie_details_url = base_url.format(id, api_key)

	with urllib.request.urlopen(get_movie_details_url) as url:
		movie_details_data = url.read()
		movie_details_response = json.loads(movie_details_data)

#creates a movie object to be used within this project using the above info
		movie_object = None
		if movie_details_response:
			id = movie_details_response.get('id')
			title = movie_details_response.get('original_title')
			overview = movie_details_response.get('overview')
			poster = movie_details_response.get('poster_path')
			vote_average = movie_details_response.get('vote_average')
			vote_count = movie_details_response.get('vote_count')

			movie_object = Movie(id, title, overview, poster, vote_average, vote_count)
	return movie_object

#allows searching of movies through (partial) movie names. movie_name is after the &query=
def search_movie(movie_name):
	search_movie_url = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(api_key, movie_name)
	with urllib.request.urlopen(search_movie_url) as url:
		search_movie_data = url.read()
		search_movie_response = json.loads(search_movie_data)

		search_movie_results = None

		if search_movie_response['results']:
			search_movie_list = search_movie_response['results']
			search_movie_results = process_results(search_movie_list)

	return search_movie_results

#processes results from def search_movie and def get_movies
def process_results(movie_list):
	movie_results = []
	for movie_item in movie_list:
		id = movie_item.get('id')
		title = movie_item.get('original_title')
		overview = movie_item.get('overview')
		poster = movie_item.get('poster_path')
		vote_average = movie_item.get('vote_average')
		vote_count = movie_item.get('vote_count')

		if poster:
			movie_object = Movie(id, title, overview, poster, vote_average, vote_count)
			movie_results.append(movie_object)

	return movie_results


