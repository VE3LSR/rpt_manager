#!/usr/bin/env python3

import yaml, sys, time

import threading, socket

import tornado.ioloop
import tornado.web

from app.allstar import allstar
from app.asterisk import asterisk

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
    with open("config.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(0)

    print (config)

    for controller in config['asterisk']:
        controller, values = list(controller.items())[0]
        if 'enabled' in values and values['enabled']:
            print("Starting controller: %s" % controller)
            print("Values: %s" % values)
            testA = asterisk(values['address'], values['port'], values['user'], values['password'])

    app = make_app()
    app.listen(config['listen_port'])
    tornado.ioloop.IOLoop.current().start()
