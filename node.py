import os
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
        self.send_packet(unicast, dst)

    def send_hello(self):
        hello = create_hello(1, 1, src_resolve[self.host])
        self.send_packet_to_neighbors(hello)

    def send_packet_to_neighbors(self, packet):
        for neighbor in nbrs[self.host]:
            self.send_packet(packet, neighbor)

    def send_packet(self, packet, destination):
        if isinstance(destination, int):
            next = routes[self.host][src_resolve[destination]]['path']
        else:
            next = routes[self.host][destination]['path']
        server = (hosts[next][0], hosts[next][1])

        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(packet, server)
        print('-->> ' + packet_type[packet[0]] + ' to ' + str(next))
        s.close()
        return 0

    def listen(self):
        print('Starting Listener')
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind((self.ip, self.port))
        while True:
            packet, addr = s.recvfrom(1024)
            pkt_type = packet[0]

            # HELLO
            if pkt_type == 1:
                seq, ttl, src = read_hello(packet)
                print('<<-- HELLO:', seq, ttl, src)


            # DATA MULTICAST
            elif pkt_type == 2:
                seq, src, n, k, ln, dests = read_data_multicast_header(packet)
                data = read_data_multicast_data(packet)
                print('<<-- DATA_MULTICAST', seq, src, n, k, ln, dests, data)


            # CENTROID REQUEST
            elif pkt_type == 3:
                seq, src, n, dests = read_centroid_request(packet)
                print('<<-- CENTROID_REQUEST', seq, src, n, dests)
                dist = 0
                for dst in dests:
                    dist += routes[self.host][src_resolve[dst]]['cost']
                dist = round(dist / len(dests))
                rep = create_centroid_reply(1, src_resolve[self.host], dist)
                self.send_packet(rep, src)


            # CENTROID REPLY
            elif pkt_type == 4:
                seq, src, mean_dist = read_centroid_reply(packet)
                print('<<-- CENTROID_REPLY', seq, src, mean_dist)


            # DATA UNICAST
            elif pkt_type == 5:
                seq, src, srccentroid, dst = read_data_unicast_header(packet)
                data = read_data_unicast_data(packet)
                print('<<-- DATA_UNICAST', seq, src, srccentroid, dst, data)
                if dst == src_resolve[self.host]:
                    ak = create_data_unicast_ack(1, src_resolve[self.host], src, srccentroid)
                    self.send_packet(ak, srccentroid)


            # MULTICAST ACK
            elif pkt_type == 6:
                seq, src, dst = read_data_multicast_ack(packet)
                print('<<-- DATA_MULTICAST_ACK', seq, src, dst)


            # UNICAST ACK
            elif pkt_type == 7:
                seq, src, dst, dstcentroid = read_data_unicast_ack(packet)
                print('<<-- DATA_UNICAST_ACK', seq, src, dst, dstcentroid)


            else:
                print('Unknown packet type')


if __name__ == '__main__':
    os.system('clear')
    node = client(sys.argv[1])

    listener = Thread(target=node.listen, args=())
    listener.start()

    node.send_hello()

    while True:
        user_in = input('$')
        cmd = user_in.split()

        if cmd[0] == 'mul':
            if int(cmd[1]) == 1:
                node.send_multicast(int(cmd[1]), int(cmd[2]), [src_resolve[cmd[3]]], cmd[4])
            elif int(cmd[1]) == 2:
                node.send_multicast(int(cmd[1]), int(cmd[2]), [src_resolve[cmd[3]], src_resolve[cmd[4]]], cmd[5])
            elif int(cmd[1]) == 3:
                node.send_multicast(int(cmd[1]), int(cmd[2]), [src_resolve[cmd[3]], src_resolve[cmd[4]], src_resolve[cmd[5]]], cmd[6])
        elif cmd[0] == 'uni':
            node.send_unicast(src_resolve[cmd[1]], cmd[2])
