# -*- coding: utf-8 -*-


import tornado.ioloop
import tornado.web
import sockjs.tornado
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

# SERVER dependency

from server_config import *

# Install ZMQ ioloop instead of a tornado ioloop
# http://zeromq.github.com/pyzmq/eventloop.html
ioloop.install()

# Socket for communication between sockets
#IPC_SOCKET = 'ipc:///tmp/zmq.ipc.sock'
#IPC_SOCKET = 'tcp://*:5555'

#BIND_SOCKET = 'tcp://*:5555'
#CONNECT_SOCKET = 'tcp://178.20.158.7:5555'

#context = zmq.Context()

class IndexHandler(tornado.web.RequestHandler):
    """Template renderer"""

    def get(self, *args, **kwargs):
        self.render('templates/sockjs-zmq-tornado-index.html')


class SocketConnection(sockjs.tornado.SockJSConnection):

    print 'SocketConnection:constructor'
    clients = set()

    # Instantiate context only once
    context = zmq.Context()
    # TODO: it will be a good idea to create in somewhere in the application init method,
    # but connection object does'nt have an access to it. Maybe we should put it into a SockRouter?

    # Публикатор сообщений.
    # Сюда должны подключиться остальные серверы для получения сообщений для рассылки
    publisher = context.socket(zmq.PUB)
    publisher.setsockopt(zmq.IDENTITY, "channel-user")
    for c in SC_CONNECT:
        print ' = connect to %s' % str(c)
        publisher.connect(c)
    publish_stream = ZMQStream(publisher)

    # Подписчик.
    # Подключается ко в
    subscriber = context.socket(zmq.SUB)
    subscriber.setsockopt(zmq.IDENTITY, "channel-user")
    subscriber.bind(SC_BIND_TCP)
    subscriber.setsockopt(zmq.SUBSCRIBE, '')

    subscribe_stream = ZMQStream(subscriber)

    def on_open(self, request):
        #subscriber = self.context.socket(zmq.PULL)
        #subscriber.connect(IPC_SOCKET)
        print 'on_open:%s' % repr(request.arguments)
        if len(self.clients) == 0:
            print ' subscribe'
            self.subscribe_stream.on_recv(self.on_receive_message)
        self.clients.add(self)

    def on_message(self, message):
        print 'on_message:%s' % str(message)
        #self.broadcast(self.clients, message)
        self.publish_stream.send_unicode(message)
        #self.publish_stream.send_unicode(message)
        #self.data["publish_stream"].send_unicode(message)

    def on_receive_message(self, message):
        print 'on_receive_message:%s' % str(message)
        #self.send(message)
        self.broadcast(self.clients, message)

    def on_close(self):
        print ':on_close'
        self.clients.remove(self)

        # Properly close ZMQ sockets
        #self.publish_stream.close()
        #self.subscribe_stream.close()

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    SocketRouter = sockjs.tornado.SockJSRouter(SocketConnection, '/socket')

    app = tornado.web.Application(
        [(r'/', IndexHandler), ] + SocketRouter.urls,
        debug=True,
        autoreload=True,
    )

    #ioloop.install()
    app.listen(8070)

    tornado.ioloop.IOLoop.instance().start()
