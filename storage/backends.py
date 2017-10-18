#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from abc import abstractmethod

import boto3

class BaseStorageBackend(object):

    @abstractmethod
    def list(self):
        raise NotImplementedError

    @abstractmethod
    def fetch(self, key):
        raise NotImplementedError

    @abstractmethod
    def save(self, file, key):
        raise NotImplementedError


class S3StorageBackend(BaseStorageBackend):

    BUCKET_NAME = 'ng-test-store'

    def __init__(self, access_key, secret_key):
        self.client = boto3.client(
            's3',
            aws_access_key_id=access_key, # 'AKIAIXJPSKN2LUQKQRKQ',
            aws_secret_access_key=secret_key # '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'
        )

    def list(self):
        res = []
        bucket = self.client.list_objects(Bucket=self.BUCKET_NAME)
        for obj in bucket['Contents']:
            res.append(obj['Key'])
        return res

    def fetch(self, key):
        return self.client.get_object(Bucket=self.BUCKET_NAME, Key=key)

    def save(self, file, key):
        self.client.upload_fileobj(file, self.BUCKET_NAME, key)
        return key


class DiskStorageBackend(BaseStorageBackend):

    UPLOAD_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Uploads')

    def list(self):
        return os.listdir(self.UPLOAD_DIR)

    def fetch(self, key):
        filepath = os.path.join(self.UPLOAD_DIR, key)
        if os.path.isfile(filepath):
            return open(filepath)

    def save(self, file, key):
        filepath = os.path.join(self.UPLOAD_DIR, key)
        file.save(filepath)
        return key
