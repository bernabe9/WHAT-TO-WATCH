from pymongo import MongoClient
import info
import requests
import json
import pprint
import time

client = MongoClient('mongodb://localhost:27017/')
db = client['what-to-watch']
movies = db.movies

def create_db_movies():
  movies.create_index("id", unique = True)

def get_movies():
  return movies

def print_all():
  for movie in movies.find():
    pprint.pprint(movie)

def get_movie_and_save(movie):
  ombd_key = 'f76a9fd7'
  movie_imdb_id = 'tt' + movie['imdbId']
  url = 'http://www.omdbapi.com/?apikey=' + ombd_key + '&i=' + movie_imdb_id
  r = requests.get(url)
  imdb_movie = r.json()
  movie = { 'id': movie['movieId'], 'name': imdb_movie['Title'], 'poster': imdb_movie['Poster'] }
  try:
    movies.insert_one(movie)
  except Exception:
    pass

def load_data():
  # Carga las primeras 100 peliculas mas populares del 2000 para adelante
  movie_ids = info.sort_movies_by_votes(info.get_movies_from(2000))
  popular_movie_ids = movie_ids[:100]
  popular_movies = info.get_movies(popular_movie_ids)
  for movie in popular_movies:
    print(movie)
    time.sleep(2)
    get_movie_and_save(movie)
