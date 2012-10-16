# -*- coding: utf-8 -*-

import motor
from tornado import gen
from bson.objectid import ObjectId


@gen.engine
def get_user(db, userid, callback):
    try:
        user = yield motor.Op(
                db['users'].find_one,
                {"_id": ObjectId(userid)}
            )
    except Exception, e:
        callback(None, e)
        return

    callback(user, None)


def get_user2(db, userid, callback):
    def on_done(res, err):
        callback(res, None)
    try:
        db['users'].find_one({"_id": ObjectId(userid)}, callback=on_done)
    except Exception, e:
        callback(None, e)


def get_user3(db, userid, callback):
    def on_done(res, err):
        callback(res, None)
    db['users'].find_one({"_id": ObjectId(userid)}, callback=on_done)


def get_user4(db, userid, callback):
    db['users'].find_one({"_id": ObjectId(userid)}, callback=callback)
