#!/usr/bin/env python3

import threading
import socket
import select
import random
import time
import re
import logging
from queue import Queue

import binascii

regx = re.compile ('^([^:\n]+): *(.*?) *\r$',re.MULTILINE)


class asteriskThread(threading.Thread):
    def __init__(self, state, work, result, ip, port, user, password):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger('RPT_Manager_CLI')
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
        self.logger.debug ("Connecting...")
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
                    self.logger.debug ("Quiting")
                    break
            if not self.work.empty():
                val = self.work.get()
                self.mySocket.send(val.encode())

            self.logger.debug ("Checking Socket")
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
#                print ('Received from server:\r\n' + buffer)
                # Find the ActionID
                aid = re.search("ActionID: (\w+)", buffer)
                if aid:
#                    print (aid.group(1))
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

    def sendNodeCmd(self, node, command):
        rnd = random.randint(1,100000)
        cmd = "ACTION: Command\r\nCOMMAND: rpt fun %s %s\r\nActionID: nodeCmd%s\r\n\r\n" % (node, command, rnd)
        self.work.put(cmd)
        while True:
            result = self.result.get(True)
            # Pull an item from the result queue - if it's ours, return it
            if 'ActionID' in result and result['ActionID'] == "nodeCmd%s" % rnd:
                # TODO: Parse the query
                return result
            else:
                self.result.put(result)

    def getNodeStat(self, node, stat="XStat"):
        rnd = random.randint(1,100000)
        cmd = "ACTION: RptStatus\r\nCOMMAND: %s\r\nNODE: %s\r\nActionID: %s%s\r\n\r\n" % (stat, node, stat, rnd)
        self.work.put(cmd)
        while True:
            result = self.result.get(True)
            # Pull an item from the result queue - if it's ours, return it
            if 'ActionID' in result and result['ActionID'] == "%s%s" % (stat, rnd):
                result_data={}
                for data in regx.findall(result['data']):
                    # TODO: 
                    if data[0] == "Conn":
                        # SawStat (https://github.com/AllStarLink/Asterisk/blob/47426d0f0ef81a5c7d181424f5bf0526a353b47a/asterisk/apps/app_rpt.c#L24138)
                        # 29372 0 342 340
                        # NODE  Keyed LastKeyed(Seconds) LastUnKeyed(Seconds)

                        # XStat (https://github.com/AllStarLink/Asterisk/blob/47426d0f0ef81a5c7d181424f5bf0526a353b47a/asterisk/apps/app_rpt.c#L24328)
                        # 29372     208.80.98.29        0           IN         38:09:44            ESTABLISHED
                        # Node      IP                  Reconnects  Direction  Connected           State
                        if "conn" not in result_data:
                            result_data['conn'] = []
                        result_data['conn'].append(data[1])
                    elif data[0] == "Var":
                        k,v = data[1].split('=')
                        result_data[k] = v
                    else:
                        result_data[data[0]] = data[1]
                return result_data
            else:
                self.result.put(result)

    def getNodeRptStat(self, node):
        rnd = random.randint(1,100000)
        cmd = "ACTION: Command\r\nCOMMAND: rpt stats %s\r\nActionID: Rptstat%s\r\n\r\n" % (node, rnd)
        self.work.put(cmd)
        while True:
            result = self.result.get(True)
            # Pull an item from the result queue - if it's ours, return it
            if 'ActionID' in result and result['ActionID'] == "Rptstat%s" % rnd:
                # Delete some lines we don't want
                
                return result
            else:
                self.result.put(result)


if __name__ == '__main__':
    testA = asterisk(IP, Port, User, Pass)
    for i in range(1):
        print ("Sending Request")

        # XStat
        result = testA.getNodeStat(29133)
        print (result)

        # SawStat
        result = testA.getNodeStat(29133, "SawStat")
        print (result)

        # NodeStat
        result = testA.getNodeStat(29133, "NodeStat")
        print (result)

        # RptStat
        result = testA.getNodeStat(29133, "RptStat")
        print (result)

#        result = testA.getNodeRptStat(29133)
#        print (result)
#        result = testA.sendNodeCmd("rpt fun 29154 #81")
#        print (result)
        time.sleep(2)

    testA.stop()
