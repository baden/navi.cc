import tornado.ioloop
import zmq
from tornado.web import Application, RequestHandler, asynchronous
from zmq.eventloop import ioloop, zmqstream
import time


class ZmqHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(ZmqHandler, self).__init__(*args, **kwargs)

        self.counter = 0
        self.requests = 10
        self.stream = None

        self.create_stream()

    def create_stream(self):
        context = zmq.Context()
        req = context.socket(zmq.REQ)
        req.connect('tcp://127.0.0.1:5000')
        self.stream = zmqstream.ZMQStream(req, tornado.ioloop.IOLoop.instance())
        self.stream.on_recv(self.receive)

    def receive(self, message):
        self.write('got: %s' % message)
        self.finish()

    @tornado.web.asynchronous
    def get(self, arg):
        print 'will send...'
        self.stream.send(str(arg))
        print 'sent.'


class TestHandler(RequestHandler):
    def reply(self):
        self.write('HTTP response')
        self.finish()

    @tornado.web.asynchronous
    def get(self, arg):
        print "Test arg", arg
        self.write("Reply")
        ioloop.IOLoop.instance().add_timeout(time.time() + 1, self.reply)
        print "Ok, time to reply"

if __name__ == "__main__":
    app = tornado.web.Application(
        [
            (r"/test/([0-9]+)", TestHandler),
            (r"/zmq/([0-9]+)", ZmqHandler)
        ])

    ioloop.install()
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
