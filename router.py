import sys
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from packets import *
from routingtable import *


class udprouter:
    def __init__(self, host):
        self.host = host
        self.ip = hosts[host][0]
        self.port = hosts[host][1]
        print('router started @ ' + self.ip + ':' + str(self.port))

    def send_packet_to_neighbors(self, packet):
        for neighbor in nbrs[self.host]:
            self.send_packet(packet, (hosts[neighbor][0], hosts[neighbor][1]))

    def send_packet(self, packet, server):
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(packet, server)
        print('Sending to:', server)
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
            print('Received pktype:' + str(pkt_type) + ' from:', addr)

            # HELLO
            if pkt_type == 1:
                seq, ttl, src = read_hello(packet)
                print(seq, ttl, src)
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
                print('recv multicast_data:')
                print(seq, src, n, k, ln, dests, data)
                # Initiate centroid finding algorithm by transmitting
                # CENTROID_REQUEST to all neighbors

                dist = 0;
                if len(dests) == 1:
                    dist = routes[self.host][src_resolve[dests]]['cost']
                else:
                    for dst in dests:
                        dist += routes[self.host][src_resolve[dst]]['cost']
                dist = round(dist / len(dests))
                costs.append((src_resolve[self.host], dist))
                centreq = create_centroid_request(1, src_resolve[self.host], n, dests)
                self.send_packet_to_neighbors(centreq)


            # CENTROID REQUEST
            elif pkt_type == 3:
                seq, src, n, dests = read_centroid_request(packet)
                print('recv centroid_request:')
                print(seq, src, n, dests)
                # Respond with CENTROID_REPLY packet to sending router with data
                # containing mean distance to specified N destination nodes
                dist = 0
                for dst in dests:
                    dist += routes[self.host][src_resolve[dst]]['cost']
                dist = round(dist / len(dests))
                rep = create_centroid_reply(1, src_resolve[self.host], dist)
                self.send_packet(rep, (hosts[src_resolve[src]][0], hosts[src_resolve[src]][1]))


            # CENTROID REPLY
            elif pkt_type == 4:
                seq, src, mean_dist = read_centroid_reply(packet)
                print('recv centroid_reply:', seq, src, mean_dist)
                #  Compare own mean distance to those in the packet and forward new
                # DATA_MULTICAST packet to minimum cost. If self, forward
                # DATA_UNICAST packets to K closest destinations out of N specified
                # and transmit DATA_MULTICAST_ACK to original sender node
                cent_reply = cent_reply + 1
                costs.append((src, mean_dist))
                print(costs)
                if cent_reply == len(nbrs[self.host]):
                    current_best_node = src_resolve[self.host]
                    current_best_cost = costs[0][1]
                    print(current_best_cost)
                    for possible in costs:
                        print(possible)
                        if possible[1] < current_best_cost:
                            print('update best')
                            current_best_node = possible[0]
                            current_best_cost = possible[1]
                        print('best node', current_best_node)

                    if current_best_node == src_resolve[self.host]:
                        # TODO select best nodes
                        for dest in s_dests:
                            uni = create_data_unicast(s_seq, s_src, src_resolve[self.host], dest, s_data)
                            self.send_packet(uni, (hosts[src_resolve[dest]][0], hosts[src_resolve[dest]][1]))

                    else:
                        forward = create_data_multicast(s_seq, s_src, s_n, s_k, s_dests, s_data)
                        self.send_packet(forward, (hosts[src_resolve[current_best_node]][0], hosts[src_resolve[current_best_node]][1]))

            # DATA UNICAST
            elif pkt_type == 5:
                seq, src, srccentroid, dst = read_data_unicast_header(packet)
                data = read_data_unicast_data(packet)
                print('recv unicast_data:')
                print(seq, src, srccentroid, dst, data)
                # Forward packet to next hop toward node destination specified. If
                # destination node, transmit DATA_UNICAST_ACK to centroid
                # destination specified
                if dst == src_resolve[self.host]:
                    ak = create_data_unicast_ack(1, src_resolve[self.host], src, srccentroid)
                    self.send_packet(ak, (hosts[src_resolve[srccentroid]][0], hosts[src_resolve[srccentroid]][1]))
                # else:
                #     print()
                #     #TODO


            # MULTICAST ACK
            elif pkt_type == 6:
                seq, src, dst = read_data_multicast_ack(packet)
                print('recv multicast_ack:')
                print(seq, src, dst)
                # Forward packet to next hop toward original sender node destination
                # specified


            # UNICAST ACK
            elif pkt_type == 7:
                seq, src, dst, dstcentroid = read_data_unicast_ack(packet)
                print('recv unicast_ack:')
                print(seq, src, dst, dstcentroid)
                # Forward packet to next hop toward centroid destination specified. If
                # centroid, wait for K such packets and transmit
                # DATA_MULTICAST_ACK toward original sender node
                uni_ack_count = uni_ack_count + 1
                if uni_ack_count == s_k:
                    multi_ack = create_data_multicast_ack(1, src_resolve[self.host], s_src)
                    self.send_packet(multi_ack, (hosts[src_resolve[s_src]][0], hosts[src_resolve[s_src]][1]))

            else:
                print('Unknown packet type')


if __name__ == '__main__':
    udp_router = udprouter(sys.argv[1])
    udp_router.handle_packets()
