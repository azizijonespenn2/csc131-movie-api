from app import myapp
from flask import jsonify, request
import json
import csv
import requests

OMDB_API_KEY = "1559debc"
OMDB_API_URL = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t="

@myapp.route('/', methods=['GET'])
def get():
    return jsonify({"Message": "Good Morning!"})


@myapp.route('/omdb', methods=['GET'])
def getdetails():
    title = str(request.json['title'])
    if title:
        req = OMDB_API_URL +  title.lower().strip().replace(' ', '+')
        res = requests.get(req)
        return res.json(), 200
    else:
        return jsonify({"Message": "Bad Request"}), 403


@myapp.route('/single', methods=['GET'])
def getmovie():
    name = str(request.json['name'])
    if name:
        results = filereader("single", name.strip())
        print(results)
        if not results:
            return jsonify({"Message": "Nothing found"}), 200
        else:
            return jsonify(results[0]), 200
    else:
        return jsonify({"Message": "Bad Request"}), 403


@myapp.route('/movies', methods=['GET'])
def getmovies():
    param = str(request.json['type'])
    input = str(request.json['value'])
    print(f'type: {param}\ninput: {input}')
    if not param or not input:
        return jsonify({"Message": "Bad Request"}), 403
    else:
        if param not in ['year', 'category', 'winner']:
            return jsonify({"Message": "Bad Request"}), 403
        results = filereader(param, input)
        if not results:
            return jsonify({"Message": "Nothing found"}), 200
        else:
            return jsonify(results), 200


@myapp.route('/movies/<param>/<input>', methods=['GET'])
def getmovieswithparams(param, input):
    if not param or not input:
        return jsonify({"Message": "Bad Request"}), 403
    else:
        if param not in ['year', 'category', 'winner']:
            return jsonify({"Message": "Bad Request"}), 403
        results = filereader(param, input)
        if not results:
            return jsonify({"Message": "Nothing found"}), 200
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
    elif param == "single":
        with open('data/owd.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                for field in line:
                    if field == input:
                        results.append({"year": line[0], "category": line[1], "winner": line[2], "entity": line[3]})
    else:
        return []
    return results
