#!/usr/bin/env python

import socket
import hashlib
import collections
import struct

bufferSize=1024
long_call_sign = 8

class ircddbgatewayRemote():

    def __init__(self, ip, port, password):
        self.ip = ip
        self.port = port
        self.password = password
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.settimeout(1.0)

    def send(self, message, response = True):
        self.sock.sendto(message, (self.ip, self.port))
        if response:
            return self.sock.recvfrom(bufferSize)
        else:
            return 

    def login(self):
        response = self.send("LIN")
        if response[0][:3] == "RND":
            seed = response[0][3:]
            # print " ".join(hex(ord(n)) for n in seed)
        else:
            print "Login Failed (RND)"
            return 1
        reply = hashlib.sha256(seed + self.password).digest()
        response = self.send("SHA%s" % reply)
        if response[0][:3] == "ACK":
            print "Login Accepted"
            return 0
        elif response[0][:3] == "NAK":
            print "Login Failed: %s" % response[0][3:]
            return 1
        else:
            print "Login Failed (UNK)"

    def getCallSigns(self):
        response = self.send("GCS")
        if response[0][:3] == "CAL":
            calls = []
            t_calls = response[0][3:]
            chunks, chunk_size = len(t_calls), 9
            for call in [ t_calls[i:i+chunk_size] for i in range(0, chunks, chunk_size) ] :
                calls.append({ "type": call[0], "call": call[1:]})
            return calls

    # Gets the details of a repeater -- Type R
    def getRepeater(self, repeater):
        response = self.send("GRP" + repeater)
        data = collections.namedtuple("Repeater", "repeater unknown reflector")
        result = data._asdict(data._make(struct.unpack('<8si8s', response[0][3:23])))
        del result['unknown']
        print result

    # Get the details of a StarNet -- Type S
    def getStarNet(self, starnet):
        print "TODO"

    # Link or unlink a repeater
    def Link(self, repeater, reflector = ""):
        if reflector == "":
            response = self.send("LNK%s" % repeater)  
        else:
            response = self.send("LNK{:12}{}".format(repeater, reflector) )
        print response[0][3:]

    def Unlink(self, repeater):
        response = self.send("LNK%s" % repeater)  
#        response = self.send("UNL%s" % repeater)  
        print response[0][3:]

    def Logout(self):
        response = self.send("LOG", False)


if __name__ == '__main__':
    test = ircddbgatewayRemote(HOST, PORT, PASSWORD)
    test.login()
    print "Getting Calls:"
    calls = test.getCallSigns()
    print calls

    print "Getting Repeater Details:"
    for call in calls:
        test.getRepeater(call["call"])

def temp():
    print "Unlinking VE3LSR C"
    test.Link("VE3LSR C")

    print "Getting Repeater Details:"
    for call in calls:
        test.getRepeater(call["call"])

    print "Linking VE3LSR C to REF030 C"
    test.Link("VE3LSR C", "REF030 C")

    print "Getting Repeater Details:"
    for call in calls:
        test.getRepeater(call["call"])

    test.Logout()
