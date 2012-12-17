# -*- coding: utf-8 -*-
from pymongo import Connection
from bson.objectid import ObjectId

__all__ = ['users']


class DB(object):
    db = None
    def __init__(self, url, replicaset=False):
        print 'DB:init'
        self.connection = Connection(url)
        self.db = self.connection.newgps

        # Создадим индексы
        self.db.users.ensure_index([
            ("method", 1),
            ("user", 1),
        ], unique=True)

    def get_user(self, cond):
        return self.db.users.find_one(cond)

    def get_user_by_id(self, id):
        return self.db.users.find_one({"_id": ObjectId(id)})


'''
def getdb(dburl, replicaset=False):
    db = None  # TODO: Пока None

    #if replicaset:
    #   c = Connection(dburl, slave_okay=True)
    c = Connection(dburl)

    db = c.newgps

    # Создадим индексы
    db.users.ensure_index([
        ("method", 1),
        ("user", 1),
    ], unique=True)
    #a = db.users.find_one({"method": "raw"})
    #print ' -init-  a:', repr(a)

    return db
'''
