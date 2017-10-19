#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.datastructures import FileStorage

from signals import storage_backend_updated


@storage_backend_updated.connect
def move_objects(app, **kwargs):
    # TODO: Make this an async task.
    from_bknd = kwargs.get('old')
    to_bknd = kwargs.get('new')
    if not (from_bknd and to_bknd) or from_bknd == to_bknd:
        return
    for key in from_bknd.list():
        to_bknd.save(FileStorage(from_bknd.fetch(key)), key)
        from_bknd.delete(key)
