from app import myapp
from flask import jsonify, request
import csv
import requests

OMDB_API_KEY = "1559debc"
OMDB_API_URL = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t="

@myapp.route('/', methods=['GET'])
def get():
    return jsonify({"Message": "Good Morning!"})


@myapp.route('/omdb', methods=['GET'])
def getdetails():
    if request.data:
        json_dict = request.get_json(force=True)
        if 'title' not in json_dict:
            return jsonify({"Message": "Bad Request"}), 400
        else:
            title = str(request.json['title'])
            if title:
                req = OMDB_API_URL +  title.lower().strip().replace(' ', '+')
                res = requests.get(req).json()

                data = {
                    "title": res['Title'],
                    "year": res['Year'],
                    "about": res['Plot'],
                    "awards": res['Awards'],
                    "image": res['Poster'],
                    "imdbId": res['imdbID'],
                    "imdbRating": res['imdbRating'],
                    "director": res['Director']
                }

                return  jsonify(data), 200
            else:
                return jsonify({"Message": "Bad Request"}), 400
    else:
        return jsonify({"Message": "Bad Request"}), 400

@myapp.route('/single', methods=['GET'])
def getmovie():
    if request.data:
        json_dict = request.get_json(force=True)
        if 'name' not in json_dict:
            return jsonify({"Message": "Bad Request"}), 400
        else:
            name = str(request.json['name'])
            if name:
                results = filereader("single", name.strip())
                print(results)
                if not results:
                    return jsonify({"Message": "Nothing found"}), 200
                else:
                    return jsonify(results[0]), 200
            else:
                return jsonify({"Message": "Bad Request"}), 400
    else:
        return jsonify({"Message": "Bad Request"}), 400

@myapp.route('/movies', methods=['GET'])
def getmovies():
    if request.data:
        json_dict = request.get_json(force=True)
        if 'type' not in json_dict or 'value' not in json_dict:
            return jsonify({"Message": "Bad Request"}), 400
        else:
            param = str(request.json['type'])
            userinput = str(request.json['value'])
            # print(f'type: {param}\nuserinput: {userinput}')
            if not param or not userinput:
                return jsonify({"Message": "Bad Request"}), 400
            else:
                if param not in ['year', 'category', 'winner']:
                    return jsonify({"Message": "Bad Request"}), 400
                results = filereader(param, userinput)
                if not results:
                    return jsonify({"Message": "Nothing found"}), 200
                else:
                    return jsonify(results), 200
    else:
        return jsonify({"Message": "Bad Request"}), 400


@myapp.route('/movies/<param>/<userinput>', methods=['GET'])
def getmovieswithparams(param, userinput):
    if not param or not userinput:
        return jsonify({"Message": "Bad Request"}), 400
    else:
        if param not in ['year', 'category', 'winner']:
            return jsonify({"Message": "Bad Request"}), 400
        results = filereader(param, userinput)
        if not results:
            return jsonify({"Message": "Nothing found"}), 200
        else:
            return jsonify(results), 200


@myapp.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return jsonify({"Message": "Invalid Request"}), 404


def filereader(param, userinput):
    results = []
    if param == "year":
        if 1993 > int(userinput) > 2017:
            return []
        with open('data/owd.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                for field in line:
                    if field == userinput:
                        results.append({"year": line[0], "category": line[1], "winner": line[2], "entity": line[3]})
    elif param == "category":
        with open('data/owd.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                for field in line:
                    if field == userinput:
                        results.append({"year": line[0], "category": line[1], "winner": line[2], "entity": line[3]})
    elif param == "winner":
        if userinput != "TRUE" and userinput != "FALSE":
            return []
        with open('data/owd.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                for field in line:
                    if field == userinput:
                        results.append({"year": line[0], "category": line[1], "winner": line[2], "entity": line[3]})
    elif param == "single":
        with open('data/owd.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                for field in line:
                    if field == userinput:
                        results.append({"year": line[0], "category": line[1], "winner": line[2], "entity": line[3]})
    else:
        return []
    return results
