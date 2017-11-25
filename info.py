import csv
from random import sample
import requests
import json
import re
import operator
import popular_movies
import pandas as pd

def generate_random_list(min, max, size):
  list = []
  for i in range(0, size):
    done = False
    while (not done):
      random_number = get_random_number(min, max)
      if random_number not in list:
        list.append(random_number)
        done = True
  return list

def get_random_number(min, max):
  return randint(min, max)

def get_movies_from(year):
  movie_ids = []
  with open('./Data/movies.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      movie_title = row['title']
      movie_year_re = re.search(r'\((\d*?)\)', movie_title)
      if movie_year_re:
        movie_year = movie_year_re.group(1)
        if int(movie_year) > year:
          movie_ids.append(row['movieId'])
  return movie_ids

def sort_movies_by_votes(index_list):
  movies = {}
  with open('./Data/ratings.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      movie_id = row['movieId']
      if movie_id in index_list:
        if movie_id in movies:
          movies[movie_id] += 1
        else:
          movies[movie_id] = 0
  sorted_movies = sorted(movies.items(), key=operator.itemgetter(1), reverse = True)
  sorted_movie_ids = list(map(lambda k: k[0], sorted_movies))
  return sorted_movie_ids

def get_movies(index_list):
  movies = []
  with open('./Data/links.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if row['movieId'] in index_list:
        movies.append(row)
  return movies

def get_suggested_movies():
  movie_ids = []
  movies = popular_movies.get_movies()
  for movie in movies.find():
    movie_ids.append(movie['id'])
  random_list = sample(movie_ids, 9)
  movies_info = []
  for index in random_list:
    movie = movies.find_one({ 'id': index })
    movie_info = { 'id': movie['id'], 'name': movie['name'], 'poster': movie['poster'] }
    movies_info.append(movie_info)
  return movies_info

def get_movies_imdb_id(movies_id):
    movies_id_posta = list(map(lambda x: str(x), movies_id))
    movies_imdb_ids = list(map(lambda x: x['imdbId'] ,get_movies(movies_id_posta)))
    return movies_imdb_ids

def get_movie_info(movie_imdb_id):
  ombd_key = 'f76a9fd7'
  movie_imdb_id = 'tt' + movie_imdb_id
  url = 'http://www.omdbapi.com/?apikey=' + ombd_key + '&i=' + movie_imdb_id
  r = requests.get(url)
  imdb_movie = r.json()
  movie = { 'name': imdb_movie['Title'], 'poster': imdb_movie['Poster'] }
  try:
    return movie
  except Exception:
    return {'fail': 'fail'}
