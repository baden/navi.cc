#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.auth
from tornado import web
from urllib import quote_plus, unquote_plus

import config



class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class Login(BaseHandler):
    def get(self):
        print repr(self.request.arguments)
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
                    '<input class="btn" type="submit" value="Sign in">'
                    '</form>'
                    '</div></div></div>'
                    '</body></html>' % quote_plus(next))

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        print "== POST: %s" % repr(self.request.arguments)
        #next = self.get_argument("next")
        next = unquote_plus(self.request.arguments.get("next")[0])
        if next:
            self.redirect(next)
        else:
            self.redirect("/")

config.router.append(('/auth/login', Login))
