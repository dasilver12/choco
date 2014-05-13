import os
import sys
import imp
from collections import namedtuple

Result = namedtuple('Result', ['type', 'content'])
choco = None
module = None

class ResultType:
    TEXT = 0
    IMAGE = 1
    LEAVE = 2

def init_module(cc, ep):
    global choco, module
    choco = cc
    module = ep

def dispatch(room, message):
    choco.dispatch(room, message, True)

def module_loader(home, config):
    for fn in os.listdir(os.path.join(home, 'modules')):
        name = os.path.basename(fn)[:-3]
        if name in config.EXCLUDED_MODULES: continue
        if fn.endswith('.py') and not fn.startswith('_'):
            fn = os.path.join(os.path.dirname(os.path.realpath(__file__)), fn)
            try: imp.load_source(name, fn)
            except Exception, e:
                print >> sys.stderr, "Error loading %s: %s" % (name, e)
                sys.exit(1)

class Cache(object):
    @staticmethod
    def get(room, name):
        key = 'choco:room:' + str(room)
        return choco.cache.hget(key, name)

    @staticmethod
    def enter(room, data):
        r = str(room)
        key = 'choco:room:' + r
        p = choco.cache.pipeline()
        p.sadd('choco:rooms', r)
        p.hset(key, 'admin', str(data['userId']))
        p.execute()

    @staticmethod
    def leave(room):
        r = str(room)
        key = 'choco:room:' + r
        p = choco.cache.pipeline()
        p.srem('choco:rooms', r)
        p.delete(key)
        p.execute()