import os

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

class FPTopo(Mininet):
    def __init__(self):
        Mininet.__init__(self, link=TCLink, controller=None, cleanup=True, )

        r1 = self.addHost('r1', inNamespace=False)
        r2 = self.addHost('r2', inNamespace=False)
        r3 = self.addHost('r3', inNamespace=False)
        r4 = self.addHost('r4', inNamespace=False)
        r5 = self.addHost('r5', inNamespace=False)

        s = self.addHost('s', inNamespace=False)
        d1 = self.addHost('d1', inNamespace=False)
        d2 = self.addHost('d2', inNamespace=False)
        d3 = self.addHost('d3', inNamespace=False)

        self.addLink(s, r1, intfName2='r1-eth0')
        self.addLink(d1, r2, intfName2='r2-eth0')
        self.addLink(d2, r4, intfName2='r4-eth0')
        self.addLink(d3, r5, intfName2='r5-eth0')

        self.addLink(r1, r2, intfName1='r1-eth1', intfName2='r2-eth1')
        self.addLink(r1, r3, intfName1='r1-eth2', intfName2='r3-eth0')
        self.addLink(r3, r4, intfName1='r3-eth1', intfName2='r4-eth1')
        self.addLink(r3, r5, intfName1='r3-eth2', intfName2='r5-eth1')
        self.addLink(r4, r5, intfName1='r4-eth2', intfName2='r5-eth2')

        r1.cmd('sysctl net.ipv4.ip_forward=1')
        r2.cmd('sysctl net.ipv4.ip_forward=1')
        r3.cmd('sysctl net.ipv4.ip_forward=1')
        r4.cmd('sysctl net.ipv4.ip_forward=1')
        r5.cmd('sysctl net.ipv4.ip_forward=1')

    def set_ips(self):
        nodeS = self.get('s')
        nodeD1 = self.get('d1')
        nodeD2 = self.get('d2')
        nodeD3 = self.get('d3')

        nodeS.setIP('10.0.1.4/16', intf='s-eth0')
        nodeD1.setIP('10.0.2.3/16', intf='d1-eth0')
        nodeD2.setIP('10.0.4.4/16', intf='d2-eth0')
        nodeD3.setIP('10.0.5.4/16', intf='d3-eth0')

        router1 = self.get('r1')
        router2 = self.get('r2')
        router3 = self.get('r3')
        router4 = self.get('r4')
        router5 = self.get('r5')

        router1.setIP('10.0.1.1/16', intf='r1-eth0')
        router1.setIP('10.0.1.2/16', intf='r1-eth1')
        router1.setIP('10.0.1.3/16', intf='r1-eth2')

        router2.setIP('10.0.2.1/16', intf='r2-eth0')
        router2.setIP('10.0.2.2/16', intf='r2-eth1')

        router3.setIP('10.0.3.1/16', intf='r3-eth0')
        router3.setIP('10.0.3.2/16', intf='r3-eth1')
        router3.setIP('10.0.3.3/16', intf='r3-eth2')

        router4.setIP('10.0.4.1/16', intf='r4-eth0')
        router4.setIP('10.0.4.2/16', intf='r4-eth1')
        router4.setIP('10.0.4.3/16', intf='r4-eth2')

        router5.setIP('10.0.5.1/16', intf='r5-eth0')
        router5.setIP('10.0.5.2/16', intf='r5-eth1')
        router5.setIP('10.0.5.3/16', intf='r5-eth2')



    def start_network(self):
        self.start()
        self.set_ips()
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
