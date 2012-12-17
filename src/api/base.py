#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.auth
import tornado.web
import tornado.escape
from tornado import gen
from urllib import quote_plus, unquote_plus

import config
# import motor
#from db import adb, users
import hashlib
from tornado.util import b
import base64


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        try:
            user = self.get_secure_cookie("user")
        except:
            user = None
        return user


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
        exist = self.db.get_user({
                'method': 'google',
                'user': user["email"]
        })
        print 'self.db.get_user result =', repr(exist)
        if exist:   # Пользователь с таким именем уже существует
            result = exist.get('_id', None)
        else:
            result = self.db.save_user({
                    'method': 'google',
                    'user': user["email"],
                    'nickname': user["name"],
                    'email': user["email"],
                    'name': user["name"],
                    'locale': user["locale"],
                    'first_name': user["first_name"],
                    'last_name': user["last_name"]
            })
            print 'self.db.save_user result =', repr(result)
        if not result:
            raise tornado.web.HTTPError(404)
        else:
            self.set_secure_cookie("user", str(result))
            self.redirect(self.get_argument("next", "/"))


class Login(BaseHandler):
    def get(self):
        # print repr(self.request.arguments)
        next = self.get_argument("next", "/")
        self.render('login.html', next=quote_plus(next))

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        user = self.get_argument("name")
        password = passhash(self.get_argument("password"))

        exist = yield adb(
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
            result = yield adb(
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
            try:
                next = unquote_plus(self.get_argument("next"))
                if next:
                    self.redirect(next)
                else:
                    self.redirect("/")
            except:  # Внешний запрос - вернем 'AUTHENTICATION_SUCCESS'
                self.write('AUTHENTICATION_SUCCESS')
                self.finish()


config.router.append(('/auth/login', Login))
config.router.append(('/auth/login/google', GoogleHandler))
