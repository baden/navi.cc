#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.auth
import tornado.web
import tornado.escape
from tornado import gen
from urllib import quote_plus, unquote_plus

import config
import motor
import hashlib
from tornado.util import b
import base64

from tornado.ioloop import IOLoop
#from queue import Queue
from Queue import Queue
# import Queue
from threading import Thread
from functools import partial


class WorkerThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs, callback = self.queue.get()
            try:
                result = func(*args, **kwargs)
                if callback is not None:
                    IOLoop.instance().add_callback(partial(callback, result))
            except Exception as e:
                print(e)
            self.queue.task_done()


class ThreadPool(object):
    def __init__(self, num_threads):
        self.queue = Queue()
        for _ in range(num_threads):
            WorkerThread(self.queue)

    def add_task(self, func, args=(), kwargs={}, callback=None):
        self.queue.put((func, args, kwargs, callback))

    def wait_completion(self):
        self.queue.join()


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def syncdb(self):
        return self.application.syncdb

    @property
    def pool(self):
        if not hasattr(self.application, 'pool'):
            self.application.pool = ThreadPool(20)
        return self.application.pool

    def get_current_user(self):
        return self.get_secure_cookie("user")


def passhash(password):
        sha1 = hashlib.sha1()
        sha1.update(tornado.escape.utf8(password))
        sha1.update(b("258EAFA5-E914-47DA-95CA-C5AB0DC85B11"))  # Magic value
        return tornado.escape.native_str(base64.b64encode(sha1.digest()))


class GoogleHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    @tornado.web.asynchronous
    @gen.engine
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        exist = yield motor.Op(
            self.db['users'].find_one,
            {
                'method': 'google',
                'user': user["email"],
            }
        )
        if exist:   # Пользователь с таким именем уже существует
            result = exist.get('_id', None)
        else:
            result = yield motor.Op(
                self.db['users'].save,
                {
                    'method': 'google',
                    'user': user["email"],
                    'nickname': user["name"],
                    'email': user["email"],
                    'name': user["name"],
                    'locale': user["locale"],
                    'first_name': user["first_name"],
                    'last_name': user["last_name"]
                }
            )
        if not result:
            raise tornado.web.HTTPError(404)
        else:
            self.set_secure_cookie("user", str(result))
            self.redirect(self.get_argument("next", "/"))


class Login(BaseHandler):
    def get(self):
        # print repr(self.request.arguments)
        next = self.get_argument("next", "/")
        self.write('<!DOCTYPE html><html><head>'
                    '<meta charset="utf-8"><title>Login</title>'
                    '<link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.0/css/bootstrap-combined.min.css" rel="stylesheet">'
                    '</head><body>'
                    '<div class="container"><div class="row"><div class="offset4 span4">'
                    '<form class="well" action="/auth/login" method="post">'
                    '<h3>Авторизация</h3>'
                    '<label>Имя:</label>'
                    '<input class="span3" placeholder="Введите имя пользователя" type="text" name="name"><br />'
                    '<label>Пароль:</label>'
                    '<input class="span3" placeholder="Введите пароль" type="password" name="password">'
                    '<input type="hidden" name="next" value="%s"><br />'
                    '<input class="btn" type="submit" value="Sign in"><a href="/auth/login/google?next=%s"><img src="/img/google-icon.png" />Войти через Google-аккаунт</a>'
                    '</form>'
                    '</div></div></div>'
                    '</body></html>' % (quote_plus(next), quote_plus(next)))

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        user = self.get_argument("name")
        password = passhash(self.get_argument("password"))

        exist = yield motor.Op(
            self.db['users'].find_one,
            {
                'method': 'raw',
                'user': user,
            }
        )
        if exist:   # Пользователь с таким именем уже существует
            if exist.get('password', '') != password:
                # raise tornado.web.HTTPError(500, 'Password is incorrect')
                self.write('<!DOCTYPE html><html><body>Пароль неверный</body></html>')
                self.finish()
                return
            result = exist.get('_id', None)
        else:
            result = yield motor.Op(
                self.db['users'].save,
                {
                    'method': 'raw',
                    'user': user,
                    'password': password,
                    'nickname': user
                }
            )

        if not result:
            raise tornado.web.HTTPError(404)
        else:
            self.set_secure_cookie("user", str(result))
            next = unquote_plus(self.get_argument("next"))
            if next:
                self.redirect(next)
            else:
                self.redirect("/")


config.router.append(('/auth/login', Login))
config.router.append(('/auth/login/google', GoogleHandler))


class DB():
    @staticmethod
    def db(dburl, replicaset=False):
        db = None  # TODO: Пока None
        if replicaset:
            db = motor.MotorReplicaSetConnection(dburl, replicaSet='navicc').open_sync().navicc
        else:
            db = motor.MotorConnection(dburl).open_sync().navicc

        # Создадим индексы
        db.users.ensure_index([
            ("method", 1),
            ("user", 1),
        ], unique=True)
        #a = db.users.find_one({"method": "raw"})
        #print ' -init-  a:', repr(a)

        return db
