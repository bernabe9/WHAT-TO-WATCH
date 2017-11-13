#AQUI VA IR EL SERVIDOR :)

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import info

app = Flask(__name__)
api = Api(app)

class Peliculas(Resource):
    def get(self):
        return {'Peliculas': 'No hay nada'} # Fetches first column that is Employee ID

class PeliculasSugerencias(Resource):
    def get(self):
        movies = info.get_suggested_movies()
        return {'movies': movies}
        

api.add_resource(Peliculas, '/pelis') # Route_1
api.add_resource(PeliculasSugerencias, '/peliculas_sugeridas') # Route_2

if __name__ == '__main__':
     app.run(port='5002')
