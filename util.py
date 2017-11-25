from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from collections import defaultdict
from surprise import Reader, Dataset, SVD, evaluate, dump
import os


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
    reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
    data = Dataset.load_from_file('./Data/ratings.csv', reader=reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.train(trainset)
    testset = trainset.build_anti_testset()
    return (algo, testset)
