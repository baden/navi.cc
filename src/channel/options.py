#

import os
import tornado.options

config_path = 'server.conf'


def options():
    tornado.options.define('debug', default=False, type=bool, help=(
        "Turn on autoreload, log to stderr only"))
    tornado.options.define('host', default='localhost', type=str, help=(
        "Server hostname"))
    tornado.options.define('port', default=8281, type=int, help=(
        "Server port"))
    tornado.options.define('cookie_secret', type=str)
    tornado.options.define('mongodb_replicaset', default=False, type=bool, help=(
        "MongoDB replicaset"))
    tornado.options.define('mongodb_url', default='localhost', type=str, help=(
        "MongoDB server url"))

    if os.path.exists(config_path):
        print 'Loading', config_path
        tornado.options.parse_config_file(config_path)
    else:
        print 'No config file at', config_path

    tornado.options.parse_command_line()
    opts = tornado.options.options
    return opts
