#!/usr/bin/python

'''
startMininet.py
*Run using python, not python3
Sets up a single switch topology in Mininet
'''

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI

# Create single switch connected to 3 hosts (Controller/Renderer/Server)
def main():
    setLogLevel('info')
    
    #Create single switch connected to n hosts
    net = Mininet(SingleSwitchTopo(n=3))
    net.start()
    
    #Start mininet Command Line Prompt
    CLI(net)
    #Stop network after exiting CLI
    net.stop()
    
    
if __name__ == '__main__':
    main()