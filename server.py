#AQUI VA IR EL SERVIDOR :)

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import info
from flask.json import jsonify
import ast
from util import get_top_n_uid, inicializar_algoritmo
from users import save_user_ratings


# Prepara el algoritmo
(algo, testset) = inicializar_algoritmo()

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('ratings', action='append')

class Peliculas(Resource):
    def get(self):
        user_id = int(request.args.get('user_id'))
        user_testset = list(filter(lambda row: row[0] == user_id, testset))
        predictions = algo.test(user_testset)
        movies_id = get_top_n_uid(predictions, user_id)
        imdb_ids = info.get_movies_imdb_id(movies_id)
        ret = []
        for imdb_id in imdb_ids:
            ret.append(info.get_movie_info(imdb_id))
        return jsonify(ret)	 # Fetches first column that is Employee ID

class PeliculasSugerencias(Resource):
    def get(self):
        movies = info.get_suggested_movies()
        return {'movies': movies}

class CalificarPeliculas(Resource):
    def post(self):
        args = parser.parse_args()
        ratings = []
        for rating in args['ratings']:
            print(ast.literal_eval(rating))
            ratings.append(ast.literal_eval(rating))
        save_user_ratings(ratings)
        return '', 204


api.add_resource(Peliculas, '/pelis') # Route_1
api.add_resource(PeliculasSugerencias, '/peliculas_sugeridas') # Route_2
api.add_resource(CalificarPeliculas, '/calificar_peliculas') # Route_3

if __name__ == '__main__':
     app.run(port='3000', threaded=True)
