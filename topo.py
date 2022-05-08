import os

from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI
from mininet.node import Node
from mininet.link import TCLink


class FPTopo(Mininet):
    def __init__(self):
        Mininet.__init__(self, link=TCLink, controller=None, cleanup=True)

        # Create Routers
        info("Creating Routers\n")
        R1 = self.addHost('R1', inNamespace=False)
        R2 = self.addHost('R2', inNamespace=False)
        R3 = self.addHost('R3', inNamespace=False)
        R4 = self.addHost('R4', inNamespace=False)
        R5 = self.addHost('R5', inNamespace=False)

        # Create Nodes
        info("Creating Nodes\n")
        S = self.addHost('S', inNamespace=False)
        D1 = self.addHost('D1', inNamespace=False)
        D2 = self.addHost('D2', inNamespace=False)
        D3 = self.addHost('D3', inNamespace=False)

        # Create Links
        info("Creating Links\n")
        # Nodes
        self.addLink(S, R1, intfName1='s-eth0', intfName2='r1-eth0')
        self.addLink(D1, R2, intfName1='d1-eth0', intfName2='r2-eth1')
        self.addLink(D2, R4, intfName1='d2-eth0', intfName2='r4-eth2')
        self.addLink(D3, R5, intfName1='d3-eth0', intfName2='r5-eth2')
        # Routers
        self.addLink(R1, R2, intfName1='r1-eth1', intfName2='r2-eth0')
        self.addLink(R1, R3, intfName1='r1-eth2', intfName2='r3-eth0')
        self.addLink(R3, R4, intfName1='r3-eth1', intfName2='r4-eth0')
        self.addLink(R3, R5, intfName1='r3-eth2', intfName2='r5-eth0')
        self.addLink(R4, R5, intfName1='r4-eth1', intfName2='r5-eth1')

        # Set IPs
        # Routers
        router1 = self.get('R1')
        router1.setIP('10.0.1.0/24', intf='r1-eth0')
        router1.setIP('10.0.1.1/24', intf='r1-eth1')
        router1.setIP('10.0.1.2/24', intf='r1-eth2')

        router2 = self.get('R2')
        router2.setIP('10.0.2.0/24', intf='r2-eth0')
        router2.setIP('10.0.2.1/24', intf='r2-eth1')

        router3 = self.get('R3')
        router3.setIP('10.0.3.0/24', intf='r3-eth0')
        router3.setIP('10.0.3.1/24', intf='r3-eth1')
        router3.setIP('10.0.3.2/24', intf='r3-eth2')

        router4 = self.get('R4')
        router4.setIP('10.0.4.0/24', intf='r4-eth0')
        router4.setIP('10.0.4.1/24', intf='r4-eth1')
        router4.setIP('10.0.4.2/24', intf='r4-eth2')

        router5 = self.get('R5')
        router5.setIP('10.0.5.0/24', intf='r5-eth0')
        router5.setIP('10.0.5.1/24', intf='r5-eth1')
        router5.setIP('10.0.5.2/24', intf='r5-eth2')

        # Nodes
        nodeS = self.get('S')
        nodeS.setIP('10.0.1.3/24', intf='s-eth0')

        nodeD1 = self.get('D1')
        nodeD1.setIP('10.0.2.2/24', intf='d1-eth0')

        nodeD2 = self.get('D2')
        nodeD2.setIP('10.0.4.3/24', intf='d2-eth0')

        nodeD3 = self.get('D3')
        nodeD3.setIP('10.0.5.3/24', intf='d3-eth0')

    def start_network(self):
        CLI(self)


def cleanup():
    os.system('sudo mn -c')
    os.system('ps aux | grep "/usr/sbin/sshd -D -o UseDNS=no -u0" > tmp')
    for line in open('tmp'):
        if line.startswith('root'):
            pid = line.split()[1]
            os.system('sudo kill -9 ' + pid)
    os.system('rm tmp')
    print('*** Terminated sshd on hosts.')


if __name__ == '__main__':
    topo = FPTopo()
    topo.start_network()
    cleanup()
