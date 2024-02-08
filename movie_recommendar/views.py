import pickle

import pandas as pd
import requests
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render

from .models import Movie


# Function to fetch poster image URL for a given movie ID
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=37190ba15b77c47a27b0613a6b07adce&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return None  # Poster not available
    except requests.exceptions.RequestException as e:
        print("Error fetching poster:", e)
        return None

movies_list = pickle.load(open('movies_list.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
movie_names =  movies['title']

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)


        return recommended_movie_names, recommended_movie_posters
    
    except IndexError:
    # Handle the case where the movie title doesn't exist
        return [], []
   

# View function for rendering the index page
def index(request):
    # Pass the movie names to the template context
    return render(request, 'index.html', {'movies': movies})


# View function for handling recommendation requests
# View function for handling recommendation requests
def recommendation(request):
    if request.method == 'GET':
        movie_title = request.GET.get('movie')
        if movie_title:
            # Call the recommend function to generate recommendations
            recommended_movie_names, recommended_movie_posters = recommend(movie_title)
            print(recommended_movie_names)

            # Zip the recommended movie names and posters together
            recommended_movies = [{'name': name, 'poster': poster} for name, poster in zip(recommended_movie_names, recommended_movie_posters)]
            
            # Return an HTTP response with the zipped list
            return render(request, 'recommendation.html', {'recommended_movies': recommended_movies})
        else:
            return HttpResponseBadRequest('Movie title not provided')
    else:
        return HttpResponseNotAllowed(['GET'])

