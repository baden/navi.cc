#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#from tornado import web, ioloop
#import tornado
from tornado import web, ioloop, gen
# import pymongo
import motor
from bson import Binary

from base64 import urlsafe_b64encode as encode
from base64 import urlsafe_b64decode as decode
from datetime import datetime


db = motor.MotorReplicaSetConnection('192.168.56.200,192.168.56.201', replicaSet = 'navicc').open_sync().test
#db = pymongo.Connection().test

counter = 2

class TestGetHandler(web.RequestHandler):
    @web.asynchronous
    @gen.engine
    def get(self, path):
        print 'Test async db read.'
        print 'path: %s' % repr(path)
        print 'arguments: %s' % repr(self.request.arguments)
        slug = 1
        #post, error = yield gen.Task(db.posts.find_one, {'slug': slug})
        post, error = yield gen.Task(db.geo.find().to_list)
        #post = db.posts.find_one()
        error = "nope"
        # print "post = ", repr(post)

        self.write('<html><body>')
        self.write('<h1>GET</h1>')
        self.write('user = %s' % self.get_secure_cookie("user"))
        self.write('<p>DB = %s</p> ' % repr(db))
        self.write('<p> host = %s</p> ' % repr(db.connection.host))
        self.write('<p>Hello test 10. res = (%s, %s)</p> ' % (post, error))
        #self.render("template.html", post = repr(post))
        self.write('</body></html>')
        self.finish()

    def post(self, path):
        print 'Test'
        print 'path: %s' % repr(path)
        print 'arguments: %s' % repr(self.request.arguments)


class TestPutHandler(web.RequestHandler):
    @web.asynchronous
    @gen.engine
    def get(self, path):
        from time import time
        from random import randint

        global counter
        self.add_header("XOrigin", "me")

        #skey = encode("I:13523466")
        skey = "I:123"
        #date = datetime.
        #sdate = datetime.datetime.utcnow()  # .date()
        #sdate = datetime.utcfromtimestamp(randint(0, int(time())))
        sdate = randint(0, int(time()))
        edate = sdate + randint(0, 600)

        #data = '\xFF\xFF\x01Hello, world\x00\xFF\xFF\x02some\x00data\xFF\xFF\xFF'
        data = ''
        #for i in xrange(32 * 60 * 60 * 24):
        for i in xrange(32):
            data += chr(i % 256)
        rec = Binary(data)

        post, error = yield gen.Task(
            # db.posts.save, {'slug': counter, 'data': rec}
            # db.posts.update, {'_id': skey}, {'$push': {date.strftime('%Y%m%d'): rec}}, True
            db.geo.save, {
                'skey': skey,
                'sdate': sdate,
                'edate': edate,
                'raw': rec
            }
        )
        counter = counter + 1
        self.write('<html><body>')
        self.write('<h1>POST</h1>')
        self.write('user = %s' % self.get_secure_cookie("user"))
        self.write('<p>DB = %s</p> ' % repr(db))
        self.write('<p> host = %s</p> ' % repr(db.connection.host))
        self.write('<p>Hello test 10. res = (%s, %s)</p> ' % (post, error))
        #self.render("template.html", post = repr(post))
        self.write('</body></html>')
        self.finish()

if __name__ == '__main__':
    TestRouter = [
      (r'/get(.*)', TestGetHandler),
      (r'/put(.*)', TestPutHandler)
    ]
    settings = {
        "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "login_url": "/login",
        "headers": {"XOrigin": "me"}
        # 'debug': True
    }
    app = web.Application(TestRouter, **settings)
    #app = web.Application(TestRouter, **settings)
    app.listen(8091)
    io_loop = ioloop.IOLoop.instance()

    print('Start application sys.executable=', sys.executable, ' sys.argv=', sys.argv)
    print('db = ', repr(db))
    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()

    print('Exit application')
