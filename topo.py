import os

from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import setLogLevel, info


class FPTopo(Mininet):
    def __init__(self):
        Mininet.__init__(self, controller=None, cleanup=True, waitConnected=True)

        r1 = self.addHost('r1', ip='192.168.0.0')
        r2 = self.addHost('r2', ip='192.168.0.1')
        r3 = self.addHost('r3', ip='192.168.0.2')
        r4 = self.addHost('r4', ip='192.168.0.3')
        r5 = self.addHost('r5', ip='192.168.0.4')

        s = self.addHost('s', ip='192.168.0.5')
        d1 = self.addHost('d1', ip='192.168.0.6')
        d2 = self.addHost('d2', ip='192.168.0.7')
        d3 = self.addHost('d3', ip='192.168.0.8')

        self.addLink(s, r1)
        self.addLink(d1, r2)
        self.addLink(d2, r4)
        self.addLink(d3, r5)

        self.addLink(r1, r2)
        self.addLink(r1, r3)
        self.addLink(r3, r4)
        self.addLink(r3, r5)
        self.addLink(r4, r5)

        rts = self.get('r1')
        rts.popen('python router.py')

    def start_network(self):
        self.start()
        CLI(self)
        self.stop()


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
    setLogLevel('info')
    topo = FPTopo()
    topo.start_network()
    cleanup()
