#!/bin/sh

#../../bin/python -m tornado.autoreload server.py
#python -m tornado.autoreload server.py
python server.py --logging=debug
echo Done

#python channel_server.py
