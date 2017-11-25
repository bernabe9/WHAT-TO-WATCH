from pymongo import MongoClient
import time

client = MongoClient('mongodb://localhost:27017/')
db = client['what-to-watch']
users_ratings = db.users_ratings

def initialize_user_id_counter():
  db.seqs.insert({
    'collection': 'users_ratings',
    'id': 671
  })

def get_next_sequence():
  ret = db.seqs.find_and_modify(
    query={ 'collection': 'users_ratings' },
    update={ '$inc': { 'id': 1 }},
    fields={ 'id': 1, '_id': 0 },
    new=True
  ).get('id')
  return ret

def get_users_ratings():
  return users_ratings

def save_user_ratings(ratings):
  user_id = get_next_sequence()
  for rating in ratings:
    user_rating = {
      'userId': user_id,
      'movieId': rating['movie_id'],
      'rating': rating['rating'],
      'timestamp': int(time.time())
    }
    users_ratings.insert_one(user_rating)
