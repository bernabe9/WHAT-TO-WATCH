import csv
from random import randint
import requests
import json

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

def get_csv_count(path):
  with open(path) as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    return sum(1 for row in reader)

def get_movies(index_list):
  movies = []
  with open('./Data/links.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
      if i in index_list:
        movies.append(row)
  return movies

## Main

def get_suggested_movies():
  row_count = get_csv_count('./Data/links.csv')
  random_list = generate_random_list(0, row_count, 9)
  movies = get_movies(random_list)
  movies_info = []
  ombd_key = 'f76a9fd7'

  for movie in movies:
    movie_imdb_id = 'tt' + movie['imdbId']
    url = 'http://www.omdbapi.com/?apikey=' + ombd_key + '&i=' + movie_imdb_id
    r = requests.get(url)
    imdb_movie = r.json()
    movie = { 'name': imdb_movie['Title'], 'poster': imdb_movie['Poster'] }
    movies_info.append(movie)

  return movies_info
