#!/usr/bin/env python
# -*- coding: utf-8 -*-
# core.py

import config
from tornado import web
from json import dumps
import base

class Version(web.RequestHandler):
    def get(self, params):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        data = {
            'version': config.versionsring,
            'user': self.current_user,
            'apisupport': [p[0] for p in config.router if p[0].startswith('/api/')],

            'path': params,
            'params': self.request.arguments,
            'arguments': repr(self.request.arguments),
            # 'cookies': repr(self.request.cookies.items()),
            'files': repr(self.request.files),
            # 'full_url': repr(self.request.full_url()),
            # 'headers': repr(self.request.headers),
            'host': self.request.host,
            'path': repr(self.request.path),
            'protocol': self.request.protocol,
            'query': repr(self.request.query),
            'remote_ip': self.request.remote_ip,
            'request_time': self.request.request_time(),
            'uri': repr(self.request.uri)
        }

        self.set_secure_cookie('api', 'secret_key')
        self.write(dumps(data, indent=2))

config.router.append((r'/api/version(.*)', Version))

print 'API:Core:import'
