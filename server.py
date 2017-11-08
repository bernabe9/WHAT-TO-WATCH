#AQUI VA IR EL SERVIDOR :)

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask.ext.jsonpify import jsonify

app = Flask(__name__)
api = Api(app)

class Peliculas(Resource):
    def get(self):
        return {'Peliculas': 'No hay nada'} # Fetches first column that is Employee ID

        

api.add_resource(Peliculas, '/pelis') # Route_1

if __name__ == '__main__':
     app.run(port='5002')
