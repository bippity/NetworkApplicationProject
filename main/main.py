#!/usr/bin/python

'''
main.py
Main program to run.
*Run using python, not python3
Will setup the mininet topology environment and instantiate the Controller/Renderer/Server
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

# Creates a simple topology of N hosts (h1 - hN), connected to single switch (s1)
class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0...N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)
            
         
def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    
    print("Testing network connectivity")
    net.pingAll()
    net.stop()
    

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()