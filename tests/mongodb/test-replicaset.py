#!/usr/bin/env python

from pymongo import Connection
from pymongo.read_preferences import ReadPreference
from pymongo import ReplicaSetConnection

#c = ReplicaSetConnection("192.168.56.102:27017", replicaSet='navicc')
#c = Connection("192.168.56.102:27017", replicaSet='navicc')
#c = Connection("192.168.56.103:27017", replicaSet='navicc')
#c = Connection("mongodb://mongodb0.navi.cc:27017,mongodb1.navi.cc:27018", replicaSet='navicc')
# c = Connection(["192.168.56.102:27017", "192.168.56.103:27017"], replicaSet='navicc')
#c = Connection("mongodb0.navi.cc:27017,mongodb1.navi.cc:27017", replicaSet='navicc')
c = ReplicaSetConnection("mongodb0.navi.cc:27017,mongodb1.navi.cc:27017", replicaSet='navicc')
#c.read_preference = ReadPreference.SECONDARY_PREFERRED
c.read_preference = ReadPreference.SECONDARY

db = c.test_database

print " db.connetcion.host = ", db.connection.host
print " is_mongos =", db.connection.is_mongos

def main():
  print "Ok: c=", repr(c)
  print "db", repr(db)
  # print "Test read from database: ", repr()

  recs = db.users.find()
  for rec in recs:
    print "rec = ", repr(rec)

  print "Test write to database"
  i = {"maha": "on"}
  # res = db.users.save(i)
  # print " res =", repr(res)

  print " db.connetcion.host = ", db.connection.host
  print " is_mongos =", db.connection.is_mongos

  c.close()
  c.disconnect()

if __name__ == "__main__":
  main()
