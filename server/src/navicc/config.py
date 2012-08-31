# -*- coding: utf-8 -*-


clients = set()
rooms = {}
ioclients = set()
imeiclients = {}

rawclients = set()
rawimeiclients = {}

import logging


# create logger with 'spam_application'
logger = logging.getLogger('channel')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('logs/channel.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
logger.info('Start application')
