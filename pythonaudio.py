import ast
import datetime
from flask import Flask, request, Response, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId

import json
from pymongo import MongoClient
from importlib.machinery import SourceFileLoader


app = Flask(__name__)


myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["AudioFiles"]
collection_song = db["Songs"]
collection_podcast = db["Podcast"]
collection_audiobook = db["AudioBook"]


@app.route('/create/<audioFileType>/', methods=['GET', 'POST'])
def create_audio(audioFileType):
    if audioFileType == '0':
        audioFileMetaData = request.get_json()
        songs = {
            'id': audioFileMetaData['id'],
            'song_name': audioFileMetaData['song_name'],
            'number_of_second': audioFileMetaData['number_of_second'],
            'upload_time': datetime.datetime.utcnow()
        }
        if len(songs['song_name']) > 100:
            return jsonify('Song name should not exceed more than 100')
        if songs['number_of_second'] < 0:
            return jsonify('Number of second must be in positive and greater or equal to 0')
        res = db['Songs'].find_one({'id': int(songs['id'])})
        if dumps(res) == 'null':
            result = db['Songs'].insert(songs)
            return jsonify('hello')
        elif dumps(res) != 'null':
            return jsonify('Id Exsits already'+str(songs['id']))
    if audioFileType == '1':
        audioFileMetaData = request.get_json()
        podcast = {
            'id': audioFileMetaData['id'],
            'podcast_name': audioFileMetaData['podcast_name'],
            'number_of_second': audioFileMetaData['number_of_second'],
            'uploaded_time': datetime.datetime.utcnow(),
            'host': audioFileMetaData['host'],
            'participant': audioFileMetaData['participant']
        }
        if len(podcast['podcast_name']) > 100:
            return jsonify('Podcast name should not exceed more than 100')
        if podcast['number_of_second'] < 0:
            return jsonify('Number of second must be in positive and greater or equal to 0')
        if len(podcast['host']) > 100:
            return jsonify('Podcast host name should not exceed more than 100')
        if podcast['participant'] > 10:
            return jsonify("Podcast participant should not exceed more than 10")
        res = db['Podcast'].find_one({'id': int(podcast['id'])})
        if dumps(res) == 'null':
            result = db['Podcast'].insert(podcast)
            return jsonify('Successfully created podcast')
        elif dumps(res) != 'null':
            return jsonify('Id Exsits already'+str(podcast['id']))

    if audioFileType == '2':
        audioFileMetaData = request.get_json()
        audiobook = {
            'id': audioFileMetaData['id'],
            'audiobook_title': audioFileMetaData['audiobook_title'],
            'auther_of_the_title': audioFileMetaData['auther_of_the_title'],
            'narrator': audioFileMetaData['narrator'],
            'number_of_second': audioFileMetaData['number_of_second'],
            'uploaded_time': datetime.datetime.utcnow()
        }
        if len(audiobook['audiobook_title']) > 100:
            return jsonify('audio book title name is exceeding more than 100')
        if len(audiobook['auther_of_the_title']) > 100:
            return jsonify('audio book auther name is exceeding more than 100')
        if len(audiobook['narrator']) > 100:
            return jsonify('audio book narrator name exceeding more than 100')
        res = db['AudioBook'].find_one({'id': int(audiobook['id'])})
        if dumps(res) == 'null':
            result = db['AudioBook'].insert(audiobook)
            return jsonify('Successfully created podcast')
        elif dumps(res) != 'null':
            return jsonify('Id Exsits already'+str(audiobook['id']))


@ app.route('/delete/<audioFileType>/<id>/', methods=['DELETE'])
def deleteApi(audioFileType, id):
    if int(audioFileType) == 0:
        result = db['Songs'].delete_one({'id': int(id)})
        if result.deleted_count > 0:
            return jsonify("Successfully deleted")
        else:
            return jsonify("id:"+id+" Does not exist")
    elif int(audioFileType) == 1:
        result = db['Podcast'].delete_one({'id': int(id)})
        if result.deleted_count > 0:
            return jsonify("Successfully deleted")
        else:
            return jsonify("id:"+id+" Does not exist")
    elif int(audioFileType) == 2:
        result = db['AudioBook'].delete_one({'id': int(id)})
        if result.deleted_count > 0:
            return jsonify("Successfully deleted")
        else:
            return jsonify("id:"+id+" Does not exist")
    else:
        return jsonify("Please enter the valid Audiotypes")


@ app.route('/read/<audioFileType>/<id>/', methods=['GET'])
def read(audioFileType, id):
    if int(audioFileType) == int(0):
        result = db['Songs'].find({'id': int(id)})
        data = []
        for res in result:
            data.append(res)
        resp = dumps(data)
        return resp
    elif int(audioFileType) == 1:
        result = db['Podcast'].find({'id': int(id)})
        data = []
        for res in result:
            data.append(res)
        resp = dumps(data)
        return resp
    elif int(audioFileType) == 2:
        result = db['AudioBook'].find({'id': int(id)})
        data = []
        for res in result:
            data.append(res)
        resp = dumps(data)
        return resp


@ app.route('/readAll/<audioFileType>/', methods=['GET'])
def readAll(audioFileType):
    if int(audioFileType) == int(0):
        result = db['Songs'].find()
        data = []
        for res in result:
            data.append(res)
        resp = dumps(data)
        return resp
    elif int(audioFileType) == 1:
        result = db['Podcast'].find()
        data = []
        for res in result:
            data.append(res)
        resp = dumps(data)
        return resp
    elif int(audioFileType) == 2:
        result = db['AudioBook'].find()
        data = []
        for res in result:
            data.append(res)
        resp = dumps(data)
        return resp
    else:
        resp = jsonify("Please enter the valid audioType")
        return resp


@ app.route('/updateAPI/<audioFileType>/<id>/', methods=['PUT'])
def updated(audioFileType, id):
    if int(audioFileType) == int(0):
        data = request.get_json()
        song_name = data['song_name']
        number_of_second = data['number_of_second']
        res = db['Songs'].find_one({"id": int(id)})
        print((dumps(res)), 'hello')
        if str(dumps(res)) == 'null':
            resp = jsonify("Id:"+id+" not found can't update")
            return resp
        elif len(dumps(res)) > int(0):
            db['Songs'].update_one({'id': int(id)}, {'$set': {
                'song_name': song_name, 'number_of_second': number_of_second, 'upload_time': datetime.datetime.utcnow()}})
            resp = jsonify("Updated Song successfully")
            return resp
    elif int(audioFileType) == int(1):
        data = request.get_json()
        podcast_name = data['podcast_name']
        number_of_second = data['number_of_second']
        host = data['host']
        participant = data['participant']
        res = db['Podcast'].find_one({"id": int(id)})
        print((dumps(res)), 'hello')
        if str(dumps(res)) == 'null':
            resp = jsonify("Id:"+id+" not found can't update")
            return resp
        elif len(dumps(res)) > int(0):
            db['Podcast'].update_one({'id': int(id)}, {'$set': {
                'podcast_name': podcast_name, 'number_of_second': number_of_second, 'uploaded_time': datetime.datetime.utcnow(), 'host': host, 'participant': participant}})
            resp = jsonify("Updated Podcast successfully")
            return resp
    elif int(audioFileType) == int(2):
        data = request.get_json()
        audiobook_title = data['audiobook_title']
        auther_of_the_title = data['auther_of_the_title']
        narrator = data['narrator']
        number_of_second = data['number_of_second']
        res = db['AudioBook'].find_one({"id": int(id)})
        if str(dumps(res)) == 'null':
            resp = jsonify("Id:"+id+" not found can't update")
            return resp
        elif len(dumps(res)) > int(0):
            db['AudioBook'].update_one({'id': int(id)}, {'$set': {
                'audiobook_title': audiobook_title, 'auther_of_the_title': auther_of_the_title, 'narrator': narrator, 'number_of_second': datetime.datetime.utcnow()}})
            resp = jsonify("Updated Audio Book successfully")
            return resp
    else:
        return jsonify("please pass the valid audio file type"+audioFileType)


if __name__ == '__main__':
    app.run(debug=True)
