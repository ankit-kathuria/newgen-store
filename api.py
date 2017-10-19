#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import send_file
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from signals import storage_backend_updated
from storage.exceptions import StorageException
from storage import receivers


app = application = Flask(__name__)
api = Api(app)

app.config.from_object('settings.Config')

file_parser = reqparse.RequestParser()
file_parser.add_argument('file', type=FileStorage, required=True, location='files')

backend_parser = reqparse.RequestParser()
backend_parser.add_argument('backend', type=str, required=True)


def update_storage_backend(backend):
    if backend.lower() not in app.config['STORAGE_BACKENDS'].keys():
        raise Exception('Invalid value provided for backend.')
    old_backend = app.config['STORAGE_ENGINE']
    new_backend = app.config['STORAGE_BACKENDS'][backend.lower()]
    app.config.update({
        'STORAGE_ENGINE': new_backend
    })
    storage_backend_updated.send(None, old=old_backend, new=new_backend)


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
        try:
            resp = storage.fetch(key)
            return send_file(resp, attachment_filename=key)
        except StorageException as e:
            raise BadRequest(e.message)

    def delete(self, key):
        storage = app.config['STORAGE_ENGINE']
        try:
            return {'key': storage.delete(key)}
        except StorageException as e:
            raise BadRequest(e.message)


class StoreAdmin(Resource):

    def post(self):
        args = backend_parser.parse_args()
        try:
            update_storage_backend(args['backend'].lower())
        except Exception as e:
            raise BadRequest(e.message)
        return {}


api.add_resource(NewgenObject, '/store/<string:key>')
api.add_resource(NewgenStore, '/store')
api.add_resource(StoreAdmin, '/admin/update-backend')


if __name__ == '__main__':
    app.run(debug=True)
