#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blinker import Namespace

event_signals = Namespace()
storage_backend_updated = event_signals.signal('storage_backend_updated')