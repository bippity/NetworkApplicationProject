

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI


def main():
    setLogLevel('info')
    
    #Create single switch connected to n hosts
    net = Mininet(SingleSwitchTopo(n=2))
    net.start()
    
    CLI(net)
    net.stop()
    
if __name__ == '__main__':
    main()
    