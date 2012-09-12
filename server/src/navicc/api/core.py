#!/usr/bin/env python
# -*- coding: utf-8 -*-
# core.py

import config
# from tornado import web
import json
from base import BaseHandler
#import motor
import tornado.web
from tornado import gen
import time
import sys
from tornado_utils.routes import route

from db import adb, users

# from callit import *
#from time import sleep

API_VERSION = 2.0
PROFILER = False

api_call_counter = 0
api_call_concurent = 0

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    profiler_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    profiler_timer = time.time


def log(s):
        print s
        sys.stdout.flush()


#config.router.append((, ApiBase))
@route(r'/api/base(.*)', name='api-base')
class ApiBase(BaseHandler):
    requred = ()
    js_pre = ''
    js_post = ''
    user = None

    #@tornado.web.asynchronous
    #@gen.engine
    def parcer(self, *args, **kwargs):
        log('    ApiBase:_parcer:start(args=%s, kwargs=%s)' % (args, kwargs))
        #sleep(0.5)

        data = {
            'answer': 'no',
            'reason': 'base api',
            'args': repr(args),
            'kwargs': repr(kwargs)
        }
        log('    ApiBase:_parcer:finish')
        kwargs["callback"](data)

    @tornado.web.asynchronous
    @gen.engine
    def api(self, *args, **kwargs):
        global api_call_counter, api_call_concurent
        api_call_counter += 1
        api_call_concurent += 1
        log('  ApiBase:api:start(args=%s, kwargs=%s)' % (args, kwargs))
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        # callback = self.request.get('callback', None)
        #callback = self.request.arguments.get('callback', None)
        callback = self.get_argument('callback', None)

        # self.current_user = "5049dbb9de72f216d3b8ec9f"

        if 'nologin' not in self.requred:
            log('    start: result = yield motor.Op...')
            #user = yield motor.Op(get_user, self.db, self.current_user)
            user = yield adb(users.get_user4, self.db, self.current_user)
            #user = yield adb(users.get_user4, self.db, "5049dbb9de72f216d3b8ec9f")
            if user:
                self.user = user.get('nickname', u'Ошибка')

            log('     done: result = yield motor.Op... [%s]' % repr(self.user))

        answ = yield gen.Task(self.parcer, *args, **kwargs)
        #answ = yield motor.Op(self.parcer, *args, **kwargs)
        # answ = self._parcer(*args, **kwargs)
        # print ' ret=', repr(answ)
        answ['api_statistics'] = {
            'call_counter': api_call_counter,
            'call_concurent': api_call_concurent
        }
        answ['user'] = self.user
        """
        res = yield adb(
                self.db['trash'].find({"i": {"$gt": 18, "$lt": 20}}).to_list
            )
        print ' === res=', repr(res)
        answ['trash'] = [
            repr(p) for p in res
        ]
        """
        if callback:
            self.write(callback + ' = ' + self.js_pre + json.dumps(answ, indent=2) + self.js_post + "\r")
        else:
            self.write(self.js_pre + json.dumps(answ, indent=2) + self.js_post + "\r")
        self.finish()
        api_call_concurent -= 1
        log('  ApiBase:api:finish')

    def get(self, *args, **kwargs):
        log('ApiBase:get:start(args=%s, kwargs=%s)' % (args, kwargs))
        self.api(*args, **kwargs)
        log('ApiBase:get:finish')

    def post(self, *args, **kwargs):
        self.api(*args, **kwargs)


#config.router.append((r'/api/version(.*)', Version))
@route(r'/api/version(.*)', name='api-version')
class Version(ApiBase):
    # requred = ('nologin')

    #@tornado.web.asynchronous
    @gen.engine
    def parcer(self, *args, **kwargs):
        log('    Version:parcer:start(args=%s, kwargs=%s)' % (args, kwargs))

        #data = self.db['trash'].find({"i": {"$gt": 18, "$lt": 20}}).to_list()
        #print ' = == data=', repr(data)
        self.application.pika.sample_message(self.request)

        data = {
            'version': config.versionsring,
            'user': self.user,
            'apisupport': [p[0] for p in config.router if p[0].startswith('/api/')],

            'pika': {
                'connected': self.application.pika.connected,
                'message': self.application.pika.get_messages()
            },

            #'path': params,
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
            'uri': repr(self.request.uri),
            'tornado': self.application.settings
        }

        #settings.set_secure_cookie('api', 'secret_key')
        log('    Version:parcer:done')
        kwargs["callback"](data)
        #callback(data)

import functools


def test_decorator(params):
    def wrap(method):

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            print 'Call test_decorator wrapper: ', repr(params)
            return method(self, *args, **kwargs)
        return wrapper
    return wrap


def test_decorator2(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        print 'Call test_decorator2 wrapper: '
        return method(self, *args, **kwargs)
    return wrapper


@route(r'/api/test(.*)', name='api-test')
@test_decorator2
class Test(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self, *args, **kwargs):
        print 'Call Test:get'
        self.write("test")
        self.finish()


print 'API:Core:import'
