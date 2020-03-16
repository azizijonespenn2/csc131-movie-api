from flask_restful import Api
from app import flaskAppInstance
from .Movie import Movie

restServer = Api(flaskAppInstance)

restServer.add_resource(Movie, "/api/v1.0/movie")

