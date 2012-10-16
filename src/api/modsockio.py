# -*- coding: utf-8 -*-

from sockjs.tornado import SockJSRouter, SockJSConnection   # , proto
import json

import config
logger = config.logger
#from config import logger


'''
    Модуль 1. Постоянное соединение
'''


class ModSock(SockJSConnection):

    def on_open(self, info):
        #print '=======+1', repr(self.session.handler), dir(self.session.handler)
        self.rooms = set()     # Список комнат, в которых мы прописаны
        config.clients.add(self)
        msg = json.dumps({
            'msg': 'newconnect',
            'data': {
                'void': 0
            }
        })
        #info.cookies['bb'] = 'hello'
        self.broadcast(config.clients, msg)
        logger.debug('mod1: open (%s)' % repr(info))

    def on_message(self, message):
        #self.broadcast(config.clients, msg)
        m = json.loads(message)
        logger.debug('mod1: Message: %s' % repr(m))
        msg = m.get('msg')
        data = m.get('data')
        if msg == 'stats':
            self.send_stats()
        elif msg == 'register':
            logger.debug('mod1: Register: %s' % repr(data['rooms']))
            for r in data['rooms']:
                self.rooms.add(r)
                if r not in config.rooms:
                    config.rooms[r] = set()
                config.rooms[r].add(self)      # Пропишем себя в комнате
        elif msg == 'unregister':
            logger.debug('mod1: Unregister: %s' % repr(data['rooms']))
            for r in data['rooms']:
                if r in self.rooms:
                    self.rooms.remove(r)
            #self.send('111')
        elif msg == 'broadcast':
            logger.debug('mod1: Broadcast: %s' % repr(data['rooms']))
            for k, v in data['rooms'].items():
                logger.debug('== %s' % repr(config.rooms[k]))
                for c in config.rooms[k]:
                    if not c.is_closed:
                        c.send(v)
        elif msg == 'command':
            cmd = data['command']
            imei = data['imei']
            logger.debug('mod1: Command: %s for %s' % (cmd, imei))
            if imei in config.imeiclients:
                if not config.imeiclients[imei].is_closed:
                    config.imeiclients[imei].stream.write(str(cmd) + '\n')


            #self.send('111')

    def on_close(self):
        for r in self.rooms:		# Вычеркнем себя из комнат
            if r in config.rooms:
                config.rooms[r].remove(self)
        config.clients.remove(self)
        logger.debug('mod1: close')

    #@classmethod
    def send_stats(self):
        info = []
        for c in config.clients:
            if not c.is_closed:
                info.append(c.log_stats())
        for c in config.ioclients:
            #if not c.is_closed:
            info.append(c.log_stats())
        rms = {}
        for k, v in config.rooms.items():
            rms[k] = [g.session.session_id for g in list(v)]
        data = {
            'clients': len(config.clients),
            'me': self.log_stats(),
            'info': info,
            'rooms': rms
        }
        self.send({
            'msg': 'stats',
            'data': data,
            'debug': {
               'self': dir(self),
               'session': dir(self.session),
               'handler': dir(self.session.handler),
               # 'add_headerr': repr(self.session.handler.add_header),
            }
        })
        logger.debug('mod1: send_stats: clients[%s]' % len(config.clients))

    @classmethod
    def dump_stats(self):
        logger.debug('mod1: stats: clients[%s]' % len(config.clients))

    #@classmethod
    def log_stats(self):
        return {
            'session_id': self.session.session_id,
            'state': repr(self.session.state),
            'conn_info': {
                'ip': self.session.conn_info.ip,
                'cookies': dict([(c, self.session.conn_info.get_cookie(c).value) for c in self.session.conn_info.cookies.keys()]),
                'arguments': repr(self.session.conn_info.arguments),
            },
            'rooms': list(self.rooms),
            'is_closed': self.session.is_closed,
        }

EchoRouter = SockJSRouter(ModSock, '/sock.*')    # Модуль 1. Постоянное соединение
