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
NodeNames = ['F22A','F22B','F22C','F22D','A400MA','A400MB','F35A','F35B','F35C','F35D']
switchContainer = []

class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=len(NodeNames) ):
        for h in range(n):
            print(NodeNames[h])
            # Each host gets 50%/#numberOfNodes of system CPU
            host = self.addHost( NodeNames[h],cpu=.5/n )
            switch = self.addSwitch( 's' + NodeNames[h] )
            # 10 Mbps, 5ms delay, 1 loss packet, 1000 packet queue
            self.addLink( host, switch)
            i = 0
            for sw in switchContainer:
                self.addLink( switch, sw, bw=10, delay= str(LinkTable[h][i])+'ms', loss=0, max_queue_size=1000, use_htb=True )
                i += 1
            switchContainer.append(switch)

def perfTest():
    "Create network and run simple performance test"
    topo = SingleSwitchTopo( n=len(NodeNames) )
    net = Mininet( topo=topo, controller = RemoteController,
               host=CPULimitedHost, link=TCLink )
    net.start()
    print "Dumping host connections"
    dumpNodeConnections( net.hosts )
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 and h4"
    h1, h4 = net.get( 'h1', 'h4' )
    net.iperf( (h1, h4) )
    #net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()
