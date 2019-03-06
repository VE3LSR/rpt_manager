#!/usr/bin/env python3

import time
import logging
import telnetlib
from queue import Queue
from threading import Thread
from datetime import datetime

#import binascii

class FourOhFourThread():
    def __init__(self, state, work, result, ip, port, user, password, login):
        self.logger = logging.getLogger('RPT_Manager_rlc404')
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.login = login
        self.state = state
        self.work = work
        self.result = result

        self.socket = telnetlib.Telnet()
        self.socket.set_debuglevel(10000)
        self.Connect()
        self.run()

        # We clear the result queue
        result = self.result.get(True)
        # TODO: We should check to make sure the login worked

    def socketWrite(self, text):
        self.socket.write((text + "\r\n").encode('ascii'))

    def Connect(self):
        self.logger.debug ("Connecting...")
        self.socket.open(self.ip, self.port)
        self.socket.read_until(b"login:")
        self.socketWrite(self.user)
        self.socket.read_until(b"Password:")
        self.socketWrite(self.password)
        self.socket.read_until(b">")
        self.socketWrite("client")
        self.socket.read_until(b"DSP4>")
        self.socketWrite(self.login)
        self.socket.read_until(b"logged in")
        self.socket.read_until(b"DSP4>")

    def logout(self):
        self.socketWrite("\030")
        self.socket.read_until(b"~>")
        self.socketWrite("exit")
        self.socket.read_all()

    def run(self):
        while True:
            time.sleep(.02)
            if not self.work.empty():
                val = self.work.get()
                print ("sending command: {}".format(val))
                self.socketWrite(val)
                self.socket.read_until(b"DSP4")
            else:
                if not self.state.empty():
                    val = self.state.get()
                    if val == "quit":
                        self.logger.debug ("Quiting")
                        self.logout()
                        break

class FourOhFour():
    def __init__(self, ip, port, user, password, login):
        self.state = Queue()
        self.work = Queue()
        self.result = Queue()
        self.worker = Thread(target=FourOhFourThread, args=(self.state, self.work, self.result, ip, port, user, password, login))
        self.worker.setDaemon(True)
        self.worker.start()

    def setTime(self):
        dt = datetime.now()
        if ("{:%p}".format(dt)) == "AM":
            dtext = '025{:%I%M}{}'.format(dt, 0)
        else:
            dtext = '025{:%I%M}{}'.format(dt, 1)
        self.work.put(dtext)


    def stop(self):
        self.state.put("quit")

if __name__ == '__main__':
    IP=""
    Port=23
    User=""
    Pass=""
    Login=""
    testA = FourOhFour(IP, Port, User, Pass, Login)
    print ("Sending Request")
    testA.setTime()
    time.sleep(2)

    testA.stop()
    time.sleep(5)

