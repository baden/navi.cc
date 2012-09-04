# -*- coding: utf-8 -*-

import os
import sys
import errno
import functools

sys.path.append(".")

import config
import base
import api

logger = config.logger

from tornado import web, ioloop, iostream, escape, options

# Перенаправление логов в файл
# options.options['log_file_prefix'].set('./logs/my_app.log')
# options.parse_command_line()

#import socket
#from sockjs.tornado import SockJSRouter, SockJSConnection, proto
#import json

import modsockio

"""
"""


class TestHandler(base.BaseHandler):
    @web.authenticated
    def get(self, path):
        print 'Test'
        print 'path: %s' % repr(path)
        print 'arguments: %s' % repr(self.request.arguments)
        user = self.get_secure_cookie("user")
        self.write('Hello %s.' % user)

    def post(self, path):
        print 'Test'
        print 'path: %s' % repr(path)
        print 'arguments: %s' % repr(self.request.arguments)
        # При регистрации будет передан идентификатор клиента в regId

'''
    Модуль 2. HTTP-управление
'''


class ModHTTP(web.RequestHandler):
    def get(self):
        id = self.get_argument('id', '')
        print 'id=', id
        self.set_header('Content-Type', 'text/plain; charset=UTF-8')
        self.write("Hello, world. ID=%s" % id)


class Clients(base.BaseHandler):
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


class Application(web.Application):
    def __init__(self):
        handlers = [
            (r'/point/test(.*)', TestHandler)
        ] + config.router
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # xsrf_cookies=True,
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            autoescape=None,
        )
        web.Application.__init__(self, handlers, **settings)

        # Единое соединение с базой данных для всех обработчиков
        self.db = None  # TODO: Пока None

if __name__ == '__main__':
    options = dict()
    if len(sys.argv) > 1:
        options['immediate_flush'] = False
    #EchoRouter = SockJSRouter(ModSock, '/sock', options)    # Модуль 1. Постоянное соединение
    '''
    TestRouter = [('/info/control', ModHTTP), ('/info/clients', Clients), (r'/test(.*)', TestHandler)]    # Модуль 2. HTTP управление
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "xsrf_cookies": True,
        "login_url": "/login",
        "headers": {"XOrigin": "me"}
        # 'debug': True
    }
    app = web.Application(modsockio.EchoRouter.urls + TestRouter + config.router, **settings)
    #app = web.Application(TestRouter, **settings)
    '''
    app = Application()
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
