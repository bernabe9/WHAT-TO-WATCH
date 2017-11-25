from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from collections import defaultdict
from surprise import Reader, Dataset, SVD, evaluate, dump
import users
import pandas as pd


def get_top_n(predictions, n=10):
    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

def get_top_n_uid(predictions, user_id, n=10):
    # First map the predictions to each user.
    top_n = []
    for uid, iid, true_r, est, _ in predictions:
        if user_id == uid: top_n.append((iid,est))
    top_n.sort(key=lambda x: x[1], reverse=True)
    top_n_ids = top_n[:n]
    return [x[0] for x in top_n_ids]

def inicializar_algoritmo():
    csv_df = pd.read_csv('Data/ratings.csv')
    users_mongo = list(users.get_users_ratings().find())
    mongo_df = pd.DataFrame(users_mongo)
    mongo_df_new = mongo_df[['userId', 'movieId', 'rating']]
    csv_df_new = csv_df[['userId', 'movieId', 'rating']]
    final_df = csv_df_new.append(mongo_df_new)
    final_df.columns = ['userID', 'itemID', 'rating']
    reader = Reader()
    data = Dataset.load_from_df(final_df, reader)
    data.split(2)  # data can now be used normally0
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.train(trainset)
    testset = trainset.build_anti_testset()
    return (algo, testset)
