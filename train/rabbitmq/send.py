#!/usr/bin/env python
import pika
from time import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World! (%f)' % time())
print " [x] Sent 'Hello World!'"
connection.close()
