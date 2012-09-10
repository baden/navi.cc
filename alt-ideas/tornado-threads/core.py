#!/usr/bin/env python
# -*- coding: utf-8 -*-
# core.py

import config
# from tornado import web
import json
from base import BaseHandler
import motor
import tornado.web
from tornado import gen
from bson import ObjectId
import time
import sys
from tornado_utils.routes import route
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


@gen.engine
def get_user(db, userid, callback):
    try:
        user = yield motor.Op(
                db['users'].find_one,
                {"_id": ObjectId(userid)}
            )
    except Exception, e:
        callback(None, e)
        return

    callback(user, None)


# config.router.append((r'/api/async/base(.*)', AsyncApiBase))
@route(r'/api/async/base(.*)', name='async-base')
class AsyncApiBase(BaseHandler):
    requred = ()
    js_pre = ''
    js_post = ''

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
        return data

    def api(self, *args, **kwargs):
        global api_call_counter, api_call_concurent
        api_call_counter += 1
        api_call_concurent += 1
        log('  ApiBase:api:start(args=%s, kwargs=%s)' % (args, kwargs))

        if 'nologin' not in self.requred:
            log('    start: result = yield motor.Op...')
            self.user = self.syncdb['users'].find_one({"_id": ObjectId(self.current_user)})
            log('     done: result = yield motor.Op... [%s]' % repr(self.user))

        answ = self.parcer(*args, **kwargs)
        answ['api_statistics'] = {
            'call_counter': api_call_counter,
            'call_concurent': api_call_concurent
        }
        answ['trash'] = [repr(p) for p in self.syncdb['trash'].find({"i": {"$gt": 18, "$lt": 20}})]

        api_call_concurent -= 1
        log('  ApiBase:api:finish')
        return answ

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        log('ApiBase:get:start(args=%s, kwargs=%s)' % (args, kwargs))
        #answ = yield tornado.gen.Task(CallIT.gen_run, self.api, *args, **kwargs)
        answ = yield gen.Task(self.pool.add_task, self.api, *args, **kwargs)
        callback = self.get_argument('callback', None)
        if callback:
            self.write(callback + ' = ' + self.js_pre + json.dumps(answ, indent=2) + self.js_post + "\r")
        else:
            self.write(self.js_pre + json.dumps(answ, indent=2) + self.js_post + "\r")
        self.finish()
        # self.api(*args, **kwargs)
        log('ApiBase:get:finish')

    #def post(self, *args, **kwargs):
    #   self.api(*args, **kwargs)


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

        if 'nologin' not in self.requred:
            log('    start: result = yield motor.Op...')
            user = yield motor.Op(get_user, self.db, self.current_user)
            if user:
                self.user = user.get('nickname', u'Ошибка')

            '''
            self.user = yield motor.Op(
                self.db['users'].find_one,
                {"_id": ObjectId(self.current_user)}
            )
            '''
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
        res = yield motor.Op(
                self.db['trash'].find({"i": {"$gt": 18, "$lt": 20}}).to_list
            )
        print ' === res=', repr(res)
        answ['trash'] = [
            repr(p) for p in res
        ]
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


class Version(ApiBase):
    # requred = ('nologin')

    #@tornado.web.asynchronous
    @gen.engine
    def parcer(self, *args, **kwargs):
        log('    Version:parcer:start(args=%s, kwargs=%s)' % (args, kwargs))

        #data = self.db['trash'].find({"i": {"$gt": 18, "$lt": 20}}).to_list()
        #print ' = == data=', repr(data)

        data = {
            'version': config.versionsring,
            'user': self.user,
            'apisupport': [p[0] for p in config.router if p[0].startswith('/api/')],

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

config.router.append((r'/api/base(.*)', ApiBase))
config.router.append((r'/api/version(.*)', Version))

print 'API:Core:import'
