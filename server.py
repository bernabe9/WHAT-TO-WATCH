#AQUI VA IR EL SERVIDOR :)

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import info
from flask.json import jsonify
import ast
from util import get_top_n_uid, inicializar_algoritmo
from users import save_user_ratings
from clasificador import Clasificador


clasificador = Clasificador()
app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('ratings', action='append')

class Peliculas(Resource):
    def get(self):
        user_id = int(request.args.get('user_id'))
        user_testset = list(filter(lambda row: row[0] == user_id, clasificador.testset))
        predictions = clasificador.algo.test(user_testset)
        movies_id = get_top_n_uid(predictions, user_id)
        imdb_ids = info.get_movies_imdb_id(movies_id)
        ret = []
        for imdb_id in imdb_ids:
            ret.append(info.get_movie_info(imdb_id))
        return jsonify(ret)

class PeliculasSugerencias(Resource):
    def get(self):
        movies = info.get_suggested_movies()
        return {'movies': movies}

class CalificarPeliculas(Resource):
    def post(self):
        args = parser.parse_args()
        ratings = []
        for rating in args['ratings']:
            ratings.append(ast.literal_eval(rating))
        user_id = save_user_ratings(ratings)
        # Entrenamos nuevamente con los nuevos datos ingresados
        clasificador.entrenar()
        return {'user_id': user_id}


api.add_resource(Peliculas, '/pelis') # Route_1
api.add_resource(PeliculasSugerencias, '/peliculas_sugeridas') # Route_2
api.add_resource(CalificarPeliculas, '/calificar_peliculas') # Route_3

if __name__ == '__main__':
     app.run(port='3000', threaded=True)
