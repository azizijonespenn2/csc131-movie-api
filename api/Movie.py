from flask_restful import Resource
import logging as logger


class Movie(Resource):

    def get(self):
        logger.debug("Inside the get method")
        return {"Message": "Inside the get method"}, 200

    def post(self):
        logger.debug("Inside the post method")
        return {"Message": "Inside the post method"}, 200

    def put(self):
        logger.debug("Inside the put method")
        return {"Message": "Inside the put method"}, 200

    def delete(self):
        logger.debug("Inside the delete method")
        return {"Message": "Inside the delete method"}, 200

