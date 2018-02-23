#!/usr/bin/env python3

import tornado.ioloop
import tornado.web

from app.allstar import allstar
from app.asterisk import asterisk
from app.config import config

class MainHandler(tornado.web.RequestHandler):

    def get(self, nodeId):
        self.set_header("Content-Type", "image/png")
        node1 = allstar(nodeId)
        self.write (node1.getBubblesImg())

def make_app():
    return tornado.web.Application([
        (r'/allstar/bubbleimage/(.*)', MainHandler),
    ])

if __name__ == "__main__":
    config = config()

    print (config)

    for controller in config['asterisk']:
        values = config['asterisk'][controller]
        if 'enabled' in values and values['enabled']:
            print("Starting controller: %s" % controller)
            print("Values: %s" % values)
            testA = asterisk(values['address'], values['port'], values['user'], values['password'])

    app = make_app()
    app.listen(config['listen_port'])
    tornado.ioloop.IOLoop.current().start()
