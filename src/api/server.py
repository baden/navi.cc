# -*- coding: utf-8 -*-

import os
import sys
import errno
import functools

#from broker import PikaClient
import zmq
from zmq.eventloop.ioloop import ZMQPoller
from zmq.eventloop import ioloop as zqioloop
#from zmq.eventloop import zmqstream
import zmqstream

sys.path.append(".")

import config
import base
#from db import getdb
from db import DB
import api

from callit import *
import logging
#import tornado.options

#logger = config.logger

from tornado import web, ioloop, iostream, escape
#from tornado import web, iostream, escape
#from tornado import options

#ioloop = zqioloop

import options

# Перенаправление логов в файл
# options.options['log_file_prefix'].set('./logs/my_app.log')
# options.parse_command_line()

#import socket
#from sockjs.tornado import SockJSRouter, SockJSConnection, proto
import json
# import pymongo

from tornado_utils.routes import route

# import modsockio

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


class ModHTTP(web.RequestHandler):
    """Модуль 2. HTTP-управление
    """

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
            # 'pstats': EchoRouter.stats.dump(),
        }
        self.set_secure_cookie('api', 'secret_key')
        self.write(json.dumps(data, indent=2))


class Application(web.Application):
    def __init__(self, opts):
        handlers = [
            (r'/point/test(.*)', TestHandler)
        ] + config.router + route.get_routes()
        # print ' Application:opts=', repr(opts)
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # xsrf_cookies=True,
            login_url="/auth/login",
            autoescape=None  # ,
            #**{k: v.value() for k, v in opts.items()}
        )
        #settings.update(opts)
        for k, v in opts.items():
            settings[k] = v.value()
        print 'settings=', repr(settings)
        web.Application.__init__(self, handlers, **settings)

        # Единое соединение с базой данных для всех обработчиков
        #self.db = base.DB.db(DB_URL, DB_REPLICASET)
        #self.db = getdb(opts.mongodb_url, opts.mongodb_replicaset)
        self.db = DB(opts.mongodb_url, opts.mongodb_replicaset)

        # Синхронная работа через pymongo
        # self.syncdb = pymongo.Connection(DB_URL).navicc

def zmqecho(msg):
    msg_json = ''.join(msg)
    print 'Received from Tornado: %s' % msg_json
    '''
    msg_data = json.loads(msg_json)
    msg_id = msg_data['msg_id']
    response = {
        'status_code': 200,
        'status_text': 'OK',
        'data': 'what up?',
        'msg_id': msg_id,
    }
    response_json = json.dumps(response)
    print 'Sending back to Tornado: %s' % (response_json)
    stream.send_multipart(response_json)
    '''

if __name__ == '__main__':
    opts = options.options()
    # print 'opts=', repr(opts)
    # print '  logging=', opts.logging
    # logging.info('WTF???')
    '''
    goptions = dict()
    if len(sys.argv) > 1:
        goptions['immediate_flush'] = False
    '''
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
    # start CallIT thread pool (Я правильно понял, что запускается 5 процессов?)
    #CallIT.start_pool(5)

    app = Application(opts)

    # Helper class PikaClient makes coding async Pika apps in tornado easy
    #pc = PikaClient()
    #app.pika = pc  # We want a shortcut for below for easier typing
    # Set our pika.log options
    #pika.log.setup(color=True)

    # tornado.options.parse_command_line()
    app.listen(opts.port)

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
    #io_loop = ioloop.IOLoop(ZMQPoller())


    ctx = zmq.Context()
    s = ctx.socket(zmq.REP)
    s.bind('ipc://127.0.0.1:5678')
    stream = zmqstream.ZMQStream(s, io_loop)
    stream.on_recv(zmqecho)



    #zloop = ioloop.IOLoop(ZMQPoller())

    # Add our Pika connect to the IOLoop with a deadline in 0.1 seconds
    #io_loop.add_timeout(time.time() + .1, app.pika.connect)

    #callback = functools.partial(modtcpip.connection_ready, sock)
    #io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    #acallback = functools.partial(moddirtcpip.connection_ready, asock)
    #io_loop.add_handler(asock.fileno(), acallback, io_loop.READ)

    logging.info('Run application')  # logging.info("starting torando web server")

    try:
        io_loop.start()
    except KeyboardInterrupt:
        #CallIT.stop_pool()
        io_loop.stop()
        logging.info('Exit application')
