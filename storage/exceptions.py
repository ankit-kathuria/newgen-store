#!/usr/bin/env python
# -*- coding: utf-8 -*-

class StorageException(Exception):
	pass

class KeyNotFoundException(StorageException):

	message = 'The provided key was not found.'
