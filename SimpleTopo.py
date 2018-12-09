#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

LinkTable = [[  -1,   1,   1,   1,  50, 100, 250, 250, 250, 250],
             [   1,  -1,   1,   1,   1,  50, 250, 250, 250, 250],
             [   1,   1,  -1,   1, 150, 100, 250, 250, 250, 250],
             [   1,   1,   1,  -1, 100, 100, 250, 250, 250, 250],
             [  50,   1, 150, 100,  -1,   1,   1,  50, 100, 150],
             [ 100,  50, 100, 100,   1,  -1,  50, 100, 100, 100],
             [ 250, 250, 250, 250,   1,  50,  -1,  10,  25,  25],
             [ 250, 250, 250, 250,  50, 100,  10,  -1,  10,  25],
             [ 250, 250, 250, 250, 100, 100,  25,  10,  -1,  10],
             [ 250, 250, 250, 250, 150, 100,  25,  25,  10,  -1]
            ]
switchContainer = []

class ATN1( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=len(LinkTable[0]) ):
        for h in range(n):
            # Each host gets 50%/#numberOfNodes of system CPU
            host = self.addHost( 'h' + str(h+1),cpu=.5/n )
            switch = self.addSwitch( 's' + str(h+1) )
            # 10 Mbps, 5ms delay, 1 loss packet, 1000 packet queue
            self.addLink( host, switch)
            i = 0
            for sw in switchContainer:
                self.addLink( switch, sw , bw=10, delay= str(LinkTable[h][i])+'ms', loss=0, max_queue_size=1000, use_htb=False )
                i += 1
            switchContainer.append(switch)

class ATN2( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=len(LinkTable[0]) ):
        for h in range(n):
            # Each host gets 50%/#numberOfNodes of system CPU
            host = self.addHost( 'h' + str(h+1),cpu=.5/n )
            switch = self.addSwitch( 's' + str(h+1) )
            # 10 Mbps, 5ms delay, 1 loss packet, 1000 packet queue
            self.addLink( host, switch)
            i = 0
            if h is not 4:#removal of host 5, 2, and 7
                for sw in switchContainer:
                    self.addLink( switch, sw , bw=10, delay= str(LinkTable[h][i])+'ms', loss=0, max_queue_size=1000, use_htb=False )
                    i += 1
                switchContainer.append(switch)

class ATN3( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=len(LinkTable[0]) ):
        for h in range(n):
            # Each host gets 50%/#numberOfNodes of system CPU
                host = self.addHost( 'h' + str(h+1),cpu=.5/n )
                switch = self.addSwitch( 's' + str(h+1) )
                # 10 Mbps, 5ms delay, 1 loss packet, 1000 packet queue
                self.addLink( host, switch)
                i = 0
                if h is not 4 and h is not 1 and h is not 6: #removal of host 5, 2, and 7
                    for sw in switchContainer:
                        self.addLink( switch, sw , bw=10, delay= str(LinkTable[h][i])+'ms', loss=0, max_queue_size=1000, use_htb=False )
                        i += 1
                    switchContainer.append(switch)

topos = { 'ATN1': ( lambda: ATN1() ), 'ATN2': ( lambda: ATN2() ), 'ATN3': ( lambda: ATN3() ) }
