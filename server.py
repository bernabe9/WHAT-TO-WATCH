#AQUI VA IR EL SERVIDOR :)

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from json import dumps
import info
from flask.json import jsonify
from util import get_top_n_uid, inicializar_algoritmo


# Prepara el algoritmo
(algo, testset) = inicializar_algoritmo()

app = Flask(__name__)
CORS(app)
api = Api(app)
print("cheto")

class Peliculas(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        user_testset = list(filter(lambda row: row[0] == user_id, testset))
        predictions = algo.test(user_testset)
        ret = get_top_n_uid(predictions, user_id)
        return jsonify(ret)	 # Fetches first column that is Employee ID

class PeliculasSugerencias(Resource):
    def get(self):
        movies = info.get_suggested_movies()
        return {'movies': movies}


api.add_resource(Peliculas, '/pelis') # Route_1
api.add_resource(PeliculasSugerencias, '/peliculas_sugeridas') # Route_2

if __name__ == '__main__':
     app.run(port='3000', threaded=True)
