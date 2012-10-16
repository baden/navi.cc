# -*- coding: utf-8 -*-
import motor

__all__ = ['users']

adb = motor.Op


def getdb(dburl, replicaset=False):
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
