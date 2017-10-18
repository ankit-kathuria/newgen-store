#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest


app = Flask(__name__)
api = Api(app)

app.config.from_object('settings.Config')

file_parser = reqparse.RequestParser()
file_parser.add_argument('file', type=FileStorage, required=True, location='files')

backend_parser = reqparse.RequestParser()
backend_parser.add_argument('backend', type=str, required=True)


def update_storage_backend(backend):
    if backend.lower() not in app.config['STORAGE_BACKENDS'].keys():
        raise Exception('Invalid value provided for backend.')
    app.config.update({
        'STORAGE_ENGINE': app.config['STORAGE_BACKENDS'][backend.lower()]
    })


class NewgenStore(Resource):

    def get(self):
        """Returns a list of all file urls.
        """
        storage = app.config['STORAGE_ENGINE']
        urls = storage.list()
        return {'files': urls}

    def post(self):
        """Upload a file and store it using the backend enabled.
        """
        storage = app.config['STORAGE_ENGINE']
        args = file_parser.parse_args()
        key = storage.save(args['file'], args['file'].filename)
        return {'key': key}

class NewgenObject(Resource):

    def get(self, key):
        storage = app.config['STORAGE_ENGINE']
        return storage.fetch(key)

    def delete(self, key):
        print key, 'inside delete'


class StoreAdmin(Resource):

    def post(self):
        args = backend_parser.parse_args()
        try:
            update_storage_backend(args['backend'].lower())
        except e:
            raise BadRequest(e.message)


api.add_resource(NewgenObject, '/store/<string:key>')
api.add_resource(NewgenStore, '/store')
api.add_resource(StoreAdmin, '/admin/update-backend')


if __name__ == '__main__':
    app.run(debug=True)
