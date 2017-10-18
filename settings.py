#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storage.backends import DiskStorageBackend, S3StorageBackend

class Config:
    DEBUG = False
    TESTING = False
    
    AWS_S3_KEYS = {
        'access_key': 'AWS-ACCESS-KEY-HERE',
        'secret_key': 'AWS-SECRET-KEY-HERE'
    }
    STORAGE_BACKENDS = {
        's3': S3StorageBackend(**AWS_S3_KEYS),
        'fs': DiskStorageBackend()
    }
    STORAGE_ENGINE = STORAGE_BACKENDS['s3']
