from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.topo import LinearTopo
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


def run():
    setLogLevel('info')
    topo = LinearTopo(k=2)  # 2 switches, 2 hosts
    net = Mininet(topo=topo, controller=RemoteController, switch=OVSSwitch)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
