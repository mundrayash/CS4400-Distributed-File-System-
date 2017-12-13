from flask import Flask
from flask_restful import Resource, Api, reqparse, request
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from bson.errors import InvalidId
import server_util

app = Flask(__name__)
api = Api(app)
files_collection = MongoClient().distrib_filesystem.ds_files
machines_collection = MongoClient().distrib_filesystem.ds_machines


class DirServerFile(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('filename')

    # Get file_id of requested file
    def get(self):
        filename = self.parser.parse_args()['filename']
        try:
            file_id = str(files_collection.find_one(
                {'file_name': filename}
            )['_id'])

        except TypeError:
            return server_util.file_missing_error(filename)

        return {'file_id': file_id}

    # Create new file listing
    def post(self):
        filename = self.parser.parse_args()['filename']
        result = files_collection.find_one({'file_name': filename})
        if result:
            return server_util.file_already_exists_error(str(result['_id']))

        else:
            try:
                target_machine_id = str(machines_collection.find_one(
                    sort=[('machine_load', ASCENDING)]
                )['_id'])

                files_collection.insert_one({
                    'file_name': filename,
                    'file_age': 1,
                    'machine_id': target_machine_id
                })

                return '', 201

            except TypeError:
                return server_util.no_servers_error()




if __name__ == '__main__':
    app.run(debug=True)