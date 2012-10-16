# -*- coding: utf-8 -*-

import os
import sys
import errno
import functools


from broker import PikaClient
import pika

sys.path.append(".")

import config
import base
from db import getdb

from callit import *
import logging
#import tornado.options

#logger = config.logger

from tornado import web, ioloop, iostream, escape
#from tornado import options

import options

# Перенаправление логов в файл
# options.options['log_file_prefix'].set('./logs/my_app.log')
# options.parse_command_line()

#import socket
#from sockjs.tornado import SockJSRouter, SockJSConnection, proto
import json
# import pymongo

from sockjs.tornado import SockJSRouter, SockJSConnection


class ChatConnection(SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    clients = set()

    def on_open(self, info):
        # Send that someone joined
        self.broadcast(self.clients, "Someone joined.")

        # Add client to the clients list
        self.clients.add(self)

    def on_message(self, message):
        # Broadcast message
        self.broadcast(self.clients, message)

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.clients.remove(self)

        self.broadcast(self.clients, "Someone left.")


class Application(web.Application):
    ticker = 0
    def __init__(self, opts):

        #handlers = [
        #    (r'/point/test(.*)', TestHandler)
        #] + config.router + route.get_routes()

        self.ChatRouter = SockJSRouter(ChatConnection, '/chat')
        print 'self.ChatRouter=', dir(self.ChatRouter)
        print '_connection=', dir(self.ChatRouter._connection)
        handlers = [] + self.ChatRouter.urls

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
        #print 'settings=', repr(settings)
        web.Application.__init__(self, handlers, **settings)

        # Единое соединение с базой данных для всех обработчиков
        #self.db = base.DB.db(DB_URL, DB_REPLICASET)
        self.db = getdb(opts.mongodb_url, opts.mongodb_replicaset)

        # Синхронная работа через pymongo
        # self.syncdb = pymongo.Connection(DB_URL).navicc
        ioloop.PeriodicCallback(self.tick, 1000).start()

    def tick(self):
        #print '-tick'
        #print 'pica=', repr(self.pika.messages)
        self.ticker += 1
        #self.ChatRouter.broadcast(self.ChatRouter._connection.clients, 'tick:%d' % self.ticker)

    def onMessage(self, body):
        #print 'onMessage:body', repr(body)
        body = json.loads(body)
        self.ChatRouter.broadcast(self.ChatRouter._connection.clients, json.dumps(body, indent=2))

if __name__ == '__main__':
    opts = options.options()

# 1. Create chat router

    # 2. Create Tornado application
    app = Application(opts)

    # Helper class PikaClient makes coding async Pika apps in tornado easy
    pc = PikaClient(app)
    app.pika = pc  # We want a shortcut for below for easier typing
    # Set our pika.log options
    pika.log.setup(color=True)

    # tornado.options.parse_command_line()
    app.listen(opts.port)

    #ioloop.PeriodicCallback(EchoConnection.dump_stats, 1000).start()
    #ioloop.IOLoop.instance().start()
    io_loop = ioloop.IOLoop.instance()

    # Add our Pika connect to the IOLoop with a deadline in 0.1 seconds
    io_loop.add_timeout(time.time() + .1, app.pika.connect)

    #io_loop.add_timeout(time.time() + 3, debug)
    logging.info('Run application')  # logging.info("starting torando web server")

    try:
        io_loop.start()
    except KeyboardInterrupt:
        #CallIT.stop_pool()
        io_loop.stop()
        logging.info('Exit application')
