#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
# import motor
from bson import Binary#!/usr/bin/env python
from time import time, sleep
import sys
import struct

#db = motor.MotorReplicaSetConnection('192.168.56.200,192.168.56.201', replicaSet = 'navicc').open_sync().test
db = pymongo.Connection('192.168.56.200,192.168.56.201', replicaSet = 'navicc').test

sdate = int(time()) - 60*60*24

def put_piece():
    global sdate
    dt = sdate
    sdate += 1
    lat = 29301234
    lon = 19301234
    raw = struct.pack('<BBIiiHBBHHBH',
        0xFF,               # 0xFF - Заголовок записи
        0xF1,               # 0xF1 - Минимальные GPS-данные
        dt,                    # Дата/время
        lat,                   # Широта
        lon,                  # Долгота
        200,                # Скорость
        42,                 # Направление (84 градуса)
        8,                      # Спутники
        1240,           # Напряжение основного аккумулятора
        421,            # Напряжение резервного аккумулятора
        1,                  #Тип точки
        0,                  # Флаги
    )
    many = ''
    for i in xrange(60*60):
        many += raw
    d ={
        'skey': '123',
        'sdate': dt,
        'edate': dt,
        #'raw': Binary(raw)
        #'raw': Binary(many)
        'raw': [Binary(raw) for i in xrange(60*60)]
    }
    db.georaw.ensure_index([('skey', pymongo.ASCENDING), ('sdate', pymongo.ASCENDING), ('edate', pymongo.ASCENDING)])
    db.georaw.save(d)

#for i in xrange(60*60*24*31):
for i in xrange(24*365):
    print '\r', (i+1),
    sys.stdout.flush()
    put_piece()
    #sleep(0.2)

# con.disconnect()
