import math
import os
import sys
from socket import socket, AF_INET, SOCK_DGRAM
from packets import *
from routingtable import *


class udprouter:
    def __init__(self, host):
        self.host = host
        self.ip = hosts[host][0]
        self.port = hosts[host][1]
        print('router started @ ' + self.ip + ':' + str(self.port))

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

    def handle_packets(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind((self.ip, self.port))
        cent_reply = 0
        uni_ack_count = 0
        costs = []
        s_seq = None
        s_src = None
        s_n = None
        s_k = None
        s_ln = None
        s_dests = None
        s_data = None
        while True:
            packet, addr = s.recvfrom(1024)
            pkt_type = packet[0]

            # HELLO
            if pkt_type == 1:
                seq, ttl, src = read_hello(packet)
                print('<<-- HELLO:', seq, ttl, src)
                # self.handle_sending(packet, (addr[0], 8881))
                # Update routing table with new destination and forward HELLO packet
                # to neighbors


            # DATA MULTICAST
            elif pkt_type == 2:
                seq, src, n, k, ln, dests = read_data_multicast_header(packet)
                data = read_data_multicast_data(packet)
                s_seq = seq
                s_src = src
                s_n = n
                s_k = k
                s_ln = ln
                s_dests = dests
                s_data = data
                uni_ack_count = 0
                cent_reply = 0
                costs = []
                print('<<-- DATA_MULTICAST', seq, src, n, k, ln, dests, data)
                # Initiate centroid finding algorithm by transmitting
                # CENTROID_REQUEST to all neighbors

                if k == 1:
                    if n == 1:
                        unic = create_data_unicast(1, src, src_resolve[self.host], dests, data)
                        self.send_packet(unic, dests)
                    else:
                        unic = create_data_unicast(1, src, src_resolve[self.host], dests[0], data)
                        self.send_packet(unic, dests[0])
                else:
                    next_nodes = []
                    total = 0
                    for dest in dests:
                        nn = src_resolve[routes[self.host][src_resolve[dest]]['path']]
                        next_nodes.append(nn)
                        total += nn
                    if total / len(dests) == next_nodes[0]:
                        print('#### Forwarding DATA_MULTICAST')
                        self.send_packet(packet, next_nodes[0])
                    else:
                        if n == k:
                            for ds in dests:
                                uni = create_data_unicast(seq, src, src_resolve[self.host], ds, data)
                                self.send_packet(uni, ds)
                        else:
                            dist = 0
                            for dst in dests:
                                dist += routes[self.host][src_resolve[dst]]['cost']
                            dist = math.ceil(dist / len(dests))
                            costs.append((src_resolve[self.host], dist))
                            centreq = create_centroid_request(1, src_resolve[self.host], n, dests)
                            for cr in next_nodes:
                                self.send_packet(centreq, cr)


            # CENTROID REQUEST
            elif pkt_type == 3:
                seq, src, n, dests = read_centroid_request(packet)
                print('<<-- CENTROID_REQUEST', seq, src, n, dests)
                # Respond with CENTROID_REPLY packet to sending router with data
                # containing mean distance to specified N destination nodes
                dist = 0
                for dst in dests:
                    dist += routes[self.host][src_resolve[dst]]['cost']
                dist = math.ceil(dist / len(dests))
                rep = create_centroid_reply(1, src_resolve[self.host], dist)
                self.send_packet(rep, src)


            # CENTROID REPLY
            elif pkt_type == 4:
                seq, src, mean_dist = read_centroid_reply(packet)
                print('<<-- CENTROID_REPLY', seq, src, mean_dist)
                #  Compare own mean distance to those in the packet and forward new
                # DATA_MULTICAST packet to minimum cost. If self, forward
                # DATA_UNICAST packets to K closest destinations out of N specified
                # and transmit DATA_MULTICAST_ACK to original sender node
                cent_reply = cent_reply + 1
                costs.append((src, mean_dist))
                if cent_reply == len(nbrs[self.host]):
                    current_best_node = src_resolve[self.host]
                    current_best_cost = costs[0][1]
                    print('costs', costs)
                    for possible in costs:
                        if possible[1] < current_best_cost:
                            current_best_node = possible[0]
                            current_best_cost = possible[1]
                    print(current_best_node)
                    forward_nodes = []
                    if current_best_node != src_resolve[self.host]:
                        for removal_canidate in s_dests:
                            if routes[self.host][removal_canidate]['path'] == src_resolve[current_best_node]:
                                forward_nodes.append(removal_canidate)
                        forward = create_data_multicast(s_seq, s_src, s_n, s_k, forward_nodes, s_data)
                        self.send_packet(forward, current_best_node)
                    else:
                        nodes_to_send = []

                        for dsts in s_dests:
                            nodes_to_send.append((dsts, routes[self.host][src_resolve[dsts]]['cost']))

                        for i in range(len(s_dests)):
                            for j in range(len(s_dests) - i - 1):
                                if nodes_to_send[j][1] > nodes_to_send[j+1][1]:
                                    temp = nodes_to_send[j]
                                    nodes_to_send[j] = nodes_to_send[j+1]
                                    nodes_to_send[j+1] = temp

                        print(nodes_to_send)
                        nodes_to_send = nodes_to_send[0:s_k]
                        for dest in nodes_to_send:
                            uni = create_data_unicast(s_seq, s_src, src_resolve[self.host], dest[0], s_data)
                            self.send_packet(uni, dest[0])


            # DATA UNICAST
            elif pkt_type == 5:
                seq, src, srccentroid, dst = read_data_unicast_header(packet)
                data = read_data_unicast_data(packet)
                print('<<-- DATA_UNICAST', seq, src, srccentroid, dst, data)
                # Forward packet to next hop toward node destination specified. If
                # destination node, transmit DATA_UNICAST_ACK to centroid
                # destination specified
                if dst == src_resolve[self.host]:
                    ak = create_data_unicast_ack(1, src_resolve[self.host], src, srccentroid)
                    self.send_packet(ak, srccentroid)
                else:
                    print('#### Forwarding DATA_UNICAST')
                    self.send_packet(packet, dst)


            # MULTICAST ACK
            elif pkt_type == 6:
                seq, src, dst = read_data_multicast_ack(packet)
                print('<<-- DATA_MULTICAST_ACK', seq, src, dst)
                if dst == src_resolve[self.host]:
                    print()
                else:
                    self.send_packet(packet, dst)
                # Forward packet to next hop toward original sender node destination
                # specified


            # UNICAST ACK
            elif pkt_type == 7:
                seq, src, dst, dstcentroid = read_data_unicast_ack(packet)
                print('<<-- DATA_UNICAST_ACK', seq, src, dst, dstcentroid)
                # Forward packet to next hop toward centroid destination specified. If
                # centroid, wait for K such packets and transmit
                # DATA_MULTICAST_ACK toward original sender node
                if dstcentroid == src_resolve[self.host]:
                    uni_ack_count = uni_ack_count + 1
                    if uni_ack_count == s_k:
                        multi_ack = create_data_multicast_ack(1, src_resolve[self.host], s_src)
                        self.send_packet(multi_ack, s_src)
                else:
                    print('#### Forwarding UNICAST_ACK')
                    self.send_packet(packet, dst)

            else:
                print('Unknown packet type')


if __name__ == '__main__':
    os.system('clear')
    udp_router = udprouter(sys.argv[1])
    udp_router.send_hello()
    udp_router.handle_packets()
