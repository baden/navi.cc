# -*- coding: utf-8 -*-

import os
import sys
import errno
import functools

sys.path.append(".")

import config
logger = config.logger


from tornado import web, ioloop, iostream, escape
#import socket
#from sockjs.tornado import SockJSRouter, SockJSConnection, proto
#import json

import modsockio

"""
"""
class TestHandler(web.RequestHandler):
    def get(self, path):
        print 'Test'
        print 'path: %s' % repr(path)
        print 'arguments: %s' % repr(self.request.arguments)
        self.write('Hello test 5.')

    def post(self, path):
        print 'Test'
        print 'path: %s' % repr(path)
        print 'arguments: %s' % repr(self.request.arguments)
        # При регистрации будет передан идентификатор клиента в regId

'''
    Модуль 2. HTTP-управление
'''
class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        print self.get_secure_cookie("user")
        return self.get_secure_cookie("user")

class Login(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        #next = self.get_argument("next")
        next = self.request.arguments.get("next")
        if next:
            self.redirect(next)
        else:
            self.redirect("/info/clients")

class ModHTTP(web.RequestHandler):
    def get(self):
        id = self.get_argument('id', '')
        print 'id=', id
        self.set_header('Content-Type', 'text/plain; charset=UTF-8')
        self.write("Hello, world. ID=%s" % id)

class Clients(BaseHandler):
    @web.authenticated
    def get(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        info = []
        for c in config.clients:
            if not c.is_closed:
                info.append(c.log_stats())

        data = {
            'name': escape.xhtml_escape(self.current_user),
            'clients': len(config.clients),
            'info': info,
            'pstats': EchoRouter.stats.dump(),
        }
        self.set_secure_cookie('api', 'secret_key')
        self.write(json.dumps(data, indent=2))

if __name__ == '__main__':
    options = dict()
    if len(sys.argv) > 1:
        options['immediate_flush'] = False
    #EchoRouter = SockJSRouter(ModSock, '/sock', options)    # Модуль 1. Постоянное соединение
    TestRouter = [('/info/control', ModHTTP), ('/info/clients', Clients), ('/login', Login), (r'/test(.*)', TestHandler)]    # Модуль 2. HTTP управление
    settings = {
        "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "login_url": "/login",
        "headers": {"XOrigin": "me"}
        # 'debug': True
    }
    app = web.Application(modsockio.EchoRouter.urls + TestRouter, **settings)
    #app = web.Application(TestRouter, **settings)
    app.listen(8080)

    '''
    # Модуль 2. Сырой TCP/IP для Магнумов
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(('', 8081))
    sock.listen(30000)
    '''

    '''
    # Модуль X. Сырой TCP/IP для Android-клиентов
    asock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    asock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    asock.setblocking(0)
    asock.bind(('', 8082))
    asock.listen(30001)
    '''

    #ioloop.PeriodicCallback(EchoConnection.dump_stats, 1000).start()
    #ioloop.IOLoop.instance().start()
    io_loop = ioloop.IOLoop.instance()

    #callback = functools.partial(modtcpip.connection_ready, sock)
    #io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    #acallback = functools.partial(moddirtcpip.connection_ready, asock)
    #io_loop.add_handler(asock.fileno(), acallback, io_loop.READ)

    logger.info('Run application')

    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()
        logger.info('Exit application')
