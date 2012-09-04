#!/bin/sh

../../server/bin/python fill-small-data.py
#python -m cProfile -o profile.pyprof test-motor.py
echo Done

#python channel_server.py
