from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os
import csv


# init app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    return jsonify({"Message": "Hello World!"})


@app.route('/movies', methods=['GET'])
def getmovies():
    param = str(request.json['type'])
    input = str(request.json['value'])
    if param not in ['year', 'category', 'winner']:
        return jsonify({"Message": "Bad Request"}), 400
    results = filereader(param, input)
    if not results:
        return jsonify({"Message": "Nothing found"}), 400
    else:
        return jsonify(results), 200


def filereader(param, input):
    results = []

    if param == "year":
        if 1993 > int(input) > 2017:
            return []
        with open('data/owd.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                for field in line:
                    if field == input:
                        results.append({"year": line[0], "category": line[1], "winner": line[2], "entity": line[3]})
    elif param == "category":
        with open('data/owd.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                for field in line:
                    if field == input:
                        results.append({"year": line[0], "category": line[1], "winner": line[2], "entity": line[3]})
    elif param == "winner":
        if input != "TRUE" and input != "FALSE":
            return []
        with open('data/owd.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                for field in line:
                    if field == input:
                        results.append({"year": line[0], "category": line[1], "winner": line[2], "entity": line[3]})
    else:
        return []

    return results


# run server
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True, use_reloader=True)



