import fresh_tomatoes
import media
import urllib2
import json

# a dictionary of movie info keyed by the IMDb.com movie id
movie_info_by_imdb_id = {
    'tt0089218': {
        'title': 'Goonies, The',
        'youtube_link': "https://www.youtube.com/watch?v=hJ2j4oWdQtU"
    },
    'tt0088000': {
        'title': 'Revenge of the Nerds',
        'youtube_link': "https://www.youtube.com/watch?v=Hw6zrInbtQE"
    },
    'tt0087538': {
        'title': 'Karate Kid, The',
        'youtube_link': "https://www.youtube.com/watch?v=n7JhKCQnEqQ"
    },
    'tt0087928': {
        'title': 'Police Academy, The',
        'youtube_link': "https://www.youtube.com/watch?v=4NT4C1F_HZE"
    },
    'tt0090142': {
        'title': 'Teen Wolf',
        'youtube_link': "https://www.youtube.com/watch?v=P6htehZchW0"
    },
    'tt0092974': {
        'title': 'Ernest Goes to Camp',
        'youtube_link': "https://www.youtube.com/watch?v=Je3jfepymQM"
    },
}

# store a sorted list of movie ids by movie title in ascending order,
#   so that they appear as such on the webpage
movies_sorted_list = sorted(movie_info_by_imdb_id.items(),
                            key=lambda tup: (tup[1]['title']))

# instantiate a list of movie objects to pass along to our web-page builder
movie_object_list = []

for movie_imdb_id, movie_info in movies_sorted_list:

    # setup a request to the OMDb api to receive a json object
    #   of movie information
    # for more info check out: http://www.omdbapi.com/
    request = urllib2.Request("http://www.omdbapi.com/?i=" +
                              movie_imdb_id +
                              "&plot=short&r=json")

    try:
        response = urllib2.urlopen(request)

    except URLError as e:
        print e.reason

    else:
        movie_data = json.load(response)

        title = movie_data['Title']
        plot = movie_data['Plot']
        poster_link = movie_data['Poster']
        youtube_link = movie_info['youtube_link']
        year_released = movie_data['Year']
        mpaa_rating = movie_data['Rated']
        runtime = movie_data['Runtime']

        movie_obj = media.Movie(title, plot, poster_link, youtube_link,
                                year_released, mpaa_rating, runtime)
        movie_object_list.append(movie_obj)

# display our movie trailers!
fresh_tomatoes.open_movies_page(movie_object_list)
