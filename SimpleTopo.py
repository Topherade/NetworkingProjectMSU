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

class ATN( Topo ):
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

def perfTest():
    "Create network and run simple performance test"
    topo = ATN( n=len(LinkTable[0]) )
    net = Mininet( topo=topo, controller = RemoteController,
               host=CPULimitedHost, link=TCLink )
    #net.start()
    #print "Dumping switch connections"
    #dumpNodeConnections( net.switches )
    #print "Testing basic network connectivity"
    #h1, h2 = net.get( 'h1', 'h2' )
    #net.ping((h1,h2))
    #print "pinging all"
    #net.pingAll()
    #print "Testing bandwidth between F22A and F35B"
    #h1, h10 = net.get( 'h1', 'h10' )
    #net.iperf( (h1, h10) )
    #net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()

topos = { 'ATN': ( lambda: ATN() ) }