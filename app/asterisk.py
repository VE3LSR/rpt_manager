#!/usr/bin/env python3

import threading
import socket
import select
import random
import time
import re
from queue import Queue

import binascii

class asteriskThread(threading.Thread):
    def __init__(self, state, work, result, ip, port, user, password):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.state = state
        self.work = work
        self.result = result
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.AsteriskConnect()
        # We clear the result queue
        result = self.result.get(True)
        # TODO: We should check to make sure the login worked

    def AsteriskConnect(self):
        print ("Connecting...")
        self.mySocket.connect((self.ip, self.port))
        login = "ACTION: LOGIN\r\nUSERNAME: %s\r\nSECRET: %s\r\nEVENTS: OFF\r\n\r\n" % (self.user, self.password)
        self.mySocket.send(login.encode())
        self.AsteriskRecv()

    def run(self):
        while True:
            if not self.state.empty():
                val = self.state.get()
                if val == "quit":
                    self.mySocket.close()
                    print ("Quiting")
                    break
            if not self.work.empty():
                val = self.work.get()
                self.mySocket.send(val.encode())

            print ("Checking Socket")
            r, w, e = select.select([self.mySocket],[],[],1.0)
            if r:
                self.AsteriskRecv()

    def AsteriskRecv(self):
        buffer = ""
        while True:
            data = self.mySocket.recv(65536).decode()
#            print (data)
#            print (binascii.hexlify(data.encode()))
            buffer += data
            if buffer[-4:] == "\r\n\r\n": 
                print ('Received from server:\r\n' + buffer)
                # Find the ActionID
                aid = re.search("ActionID: (\w+)", buffer)
                if aid:
                    print (aid.group(1))
                    self.result.put({'ActionID': aid.group(1), 'data':buffer})
                else:
                    self.result.put({'data':buffer})
                return True

class asterisk():
    def __init__(self, ip, port, user, password):
        self.state = Queue()
        self.work = Queue()
        self.result = Queue()
        self.thread = asteriskThread(self.state, self.work, self.result, ip, port, user, password)
        self.thread.start()

    def stop(self):
        self.state.put("quit")

    def getNodeXStat(self, node):
        rnd = random.randint(1,100000)
        cmd = "ACTION: RptStatus\r\nCOMMAND: XStat\r\nNODE: %s\r\nActionID: xstat%s\r\n\r\n" % (node, rnd)
        self.work.put(cmd)
        while True:
            result = self.result.get(True)
            # Pull an item from the result queue - if it's ours, return it
            if 'ActionID' in result and result['ActionID'] == "xstat%s" % rnd:
                # TODO: Parse the query
                return result
            else:
                self.result.put(result)

    def sendNodeCmd(self, command):
        rnd = random.randint(1,100000)
        cmd = "ACTION: Command\r\nCOMMAND: %s\r\nActionID: nodeCmd%s\r\n\r\n" % (command, rnd)
        self.work.put(cmd)
        while True:
            result = self.result.get(True)
            # Pull an item from the result queue - if it's ours, return it
            if 'ActionID' in result and result['ActionID'] == "nodeCmd%s" % rnd:
                # TODO: Parse the query
                return result
            else:
                self.result.put(result)

    def getNodeSawStat(self, node):
        rnd = random.randint(1,100000)
        cmd = "ACTION: RptStatus\r\nCOMMAND: SawStat\r\nNODE: %s\r\nActionID: Sawstat%s\r\n\r\n" % (node, rnd)
        self.work.put(cmd)
        while True:
            result = self.result.get(True)
            # Pull an item from the result queue - if it's ours, return it
            if 'ActionID' in result and result['ActionID'] == "Sawstat%s" % rnd:
                # TODO: Parse the query
                return result
            else:
                self.result.put(result)


if __name__ == '__main__':
    testA = asterisk("IP", Port, "USER", "PASS")
    for i in range(1):
        print ("Sending Request")
        result = testA.getNodeXStat(29133)
        print (result)
        result = testA.getNodeSawStat(29133)
        print (result)
#        result = testA.sendNodeCmd("rpt fun 29154 #81")
#        print (result)
        time.sleep(2)

    testA.stop()
