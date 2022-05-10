import sys
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
from packets import *
from routingtable import *


class client:
    def __init__(self, host):
        self.host = host
        self.ip = hosts[host][0]
        self.port = hosts[host][1]
        print('node started @ ' + self.ip + ':' + str(self.port))

    def send_multicast(self, n, k, dsts, data):
        mlcast = create_data_multicast(1, src_resolve[self.host], n, k, dsts, data)
        self.send_packet_to_neighbors(mlcast)

    def send_unicast(self, dst, data):
        unicast = create_data_unicast(1, src_resolve[self.host], src_resolve[self.host], dst, data)
        self.send_packet(unicast, (hosts[src_resolve[dst]][0], hosts[src_resolve[dst]][1]))

    def send_hello(self):
        hello = create_hello(1, 1, src_resolve[self.host])
        self.send_packet_to_neighbors(hello)

    def send_packet_to_neighbors(self, packet):
        for neighbor in nbrs[self.host]:
            self.send_packet(packet, (hosts[neighbor][0], hosts[neighbor][1]))

    def send_packet(self, packet, dst):
        s = socket(AF_INET, SOCK_DGRAM)
        #nx_node = routes[self.host][dst]['path']
        s.sendto(packet, dst)
        print('Sent packet type ' + str(packet[0]) + ' to ' + str(dst))
        s.close()
        return 0

    def listen(self):
        print('Listening')
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind((self.ip, self.port))
        while True:
            packet, addr = s.recvfrom(1024)
            print('Recieved from:', addr)
            pkt_type = packet[0]

            # HELLO
            if pkt_type == 1:
                seq, ttl, src = read_hello(packet)
                print('recv hello:')
                print(seq, ttl, src)


            # DATA MULTICAST
            elif pkt_type == 2:
                seq, src, n, k, ln, dests = read_data_multicast_header(packet)
                data = read_data_multicast_data(packet)
                print('recv multicast_data')
                print(seq, src, n, k, ln, dests, data)


            # CENTROID REQUEST
            elif pkt_type == 3:
                seq, src, n, dests = read_centroid_request(packet)
                print('recv centroid_request')
                print(seq, src, n, dests)
                dist = 0
                for dst in dests:
                    dist += routes[self.host][src_resolve[dst]]['cost']
                dist = round(dist / len(dests))
                rep = create_centroid_reply(1, src_resolve[self.host], dist)
                self.send_packet(rep, (hosts[src_resolve[src]][0], hosts[src_resolve[src]][1]))


            # CENTROID REPLY
            elif pkt_type == 4:
                seq, src, mean_dist = read_centroid_reply(packet)
                print('recv centroid_reply')
                print(seq, src, mean_dist)


            # DATA UNICAST
            elif pkt_type == 5:
                seq, src, srccentroid, dst = read_data_unicast_header(packet)
                data = read_data_unicast_data(packet)
                print('recv unicast_data')
                print(seq, src, srccentroid, dst, data)
                if dst == src_resolve[self.host]:
                    ak = create_data_unicast_ack(1, src_resolve[self.host], src, srccentroid)
                    self.send_packet(ak, (hosts[src_resolve[srccentroid]][0], hosts[src_resolve[srccentroid]][1]))


            # MULTICAST ACK
            elif pkt_type == 6:
                seq, src, dst = read_data_multicast_ack(packet)
                print('recv multiack')
                print(seq, src, dst)


            # UNICAST ACK
            elif pkt_type == 7:
                seq, src, dst, dstcentroid = read_data_unicast_ack(packet)
                print('recv uniack')
                print(seq, src, dst, dstcentroid)


            else:
                print('Unknown packet type')


if __name__ == '__main__':
    node = client(sys.argv[1])

    listener = Thread(target=node.listen, args=())
    listener.start()

    node.send_hello()

    # if (sys.argv[1] == 's'):
    #     node.send_multicast(3, 3, [7, 8, 9], 'sdfa')

    # cr = create_centroid_request(1, src_resolve[sys.argv[1]], 3, [7, 8, 9])
    # node.send_packet_to_neighbors(cr)
    #
    # crreply = create_centroid_reply(1, src_resolve[sys.argv[1]], 2)
    # node.send_packet_to_neighbors(crreply)
    #
    # un = create_data_unicast(1, src_resolve[sys.argv[1]], src_resolve[sys.argv[1]], src_resolve[sys.argv[1]], 'sdfaf')
    # node.send_packet_to_neighbors(un)
    #
    # mulack = create_data_multicast_ack(1, src_resolve[sys.argv[1]], src_resolve[sys.argv[1]])
    # node.send_packet_to_neighbors(mulack)
    #
    # uniack = create_data_unicast_ack(1, src_resolve[sys.argv[1]], src_resolve[sys.argv[1]], src_resolve[sys.argv[1]])
    # node.send_packet_to_neighbors(uniack)

    while True:
        user_in = input('>')
        cmd = user_in.split()

        if cmd[0] == 'mul':
            if int(cmd[1]) == 1:
                node.send_multicast(int(cmd[1]), int(cmd[2]), [int(cmd[3])], cmd[4])
            elif int(cmd[1]) == 2:
                node.send_multicast(int(cmd[1]), int(cmd[2]), [int(cmd[3]), int(cmd[4])], cmd[5])
            elif int(cmd[1]) == 3:
                node.send_multicast(int(cmd[1]), int(cmd[2]), [int(cmd[3]), int(cmd[4]), int(cmd[5])], cmd[6])
        elif cmd[0] == 'uni':
            node.send_unicast(int(cmd[1]), cmd[2])
