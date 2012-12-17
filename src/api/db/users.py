# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

#def get_user(db, userid):
#    return db['users'].find_one({"_id": ObjectId(userid)})

def get_user(db, cond):
    return db['users'].find_one(cond)
