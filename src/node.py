import sys
import os
import requests

from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import ObjectId
import server_util

app = Flask(__name__)
api = Api(app)
files_collection = MongoClient().distrib_filesystem.node_files

DS_ADDR = ('127.0.0.1', 5000)


class FileServer(Resource):
    def get(self, file_id):
        file_text = files_collection.find_one(
            {'_id': ObjectId(file_id)}
        )['file_text']

        return {'file': file_text}, 200

    def post(self, file_id):
        new_text = request.get_json()['data']
        files_collection.update_one(
            {'_id': ObjectId(file_id)},
            {'$set': {'file_text': new_text}},
            upsert=True
        )
        return '', 204


api.add_resource(FileServer, '/<string:file_id>')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            print('Initing node')
            requests.post(
                server_util.url_builder(DS_ADDR[0], DS_ADDR[1], 'config'),
                json={'ip': sys.argv[1], 'port': sys.argv[2]}
            )

        app.run(debug=True, host=sys.argv[1], port=int(sys.argv[2]))
        requests.delete(
            server_util.url_builder(DS_ADDR[0], DS_ADDR[1], 'config'),
            json={'ip': sys.argv[1], 'port': sys.argv[2]}
        )

        # Catastrophic delete EVERYTHING if node goes down! (Purposeful)
        files_collection.delete_many({})
    else:
        print('Supply an IP and Port')