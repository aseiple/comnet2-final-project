from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from packets import *

class udprouter:
    def __init__(self, id, port, rt):
        self.port = port
        self.id = id
        self.rt = rt

    def search_dst_addr(self, dst):
        for x in range(len(self.rt['routes'])):
            if self.rt['routes'][x]['id'] == dst:
                return (self.rt['routes'][x]['ip'], self.rt['routes'][x]['port'])
        return ('10.0.1.1', 8882)

    def handle_sending(self, packet, server):
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(packet, server)
        print('Sending to:', server)
        s.close()
        return 0

    def handle_packets(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('0.0.0.0', self.port))
        while True:
            packet, addr = s.recvfrom(1024)
            print('Received from:', addr)
            pkt_type = packet[1]
            if pkt_type == 1:
                seq, ttl, src = read_hello(packet)
                print(src)
                self.handle_sending(packet, (addr[0], 8881))
                # Update routing table with new destination and forward HELLO packet
                # to neighbors
            elif pkt_type == 2:
                seq, src, n, k, ln, dests = read_data_multicast_header(packet)
                data = read_data_multicast_data(packet)
                # Initiate centroid finding algorithm by transmitting
                # CENTROID_REQUEST to all neighbors
            elif pkt_type == 3:
                seq, src, n, dests = read_centroid_request(packet)
                # Respond with CENTROID_REPLY packet to sending router with data
                # containing mean distance to specified N destination nodes
            elif pkt_type == 4:
                seq, src, mean_dist = read_centroid_reply(packet)
                #  Compare own mean distance to those in the packet and forward new
                # DATA_MULTICAST packet to minimum cost. If self, forward
                # DATA_UNICAST packets to K closest destinations out of N specified
                # and transmit DATA_MULTICAST_ACK to original sender node
            elif pkt_type == 5:
                seq, src, srccentroid, dst = read_data_unicast_header(packet)
                data = read_data_unicast_data(packet)
                # Forward packet to next hop toward node destination specified. If
                # destination node, transmit DATA_UNICAST_ACK to centroid
                # destination specified
            elif pkt_type == 6:
                seq, src, dst = read_data_multicast_ack(packet)
                # Forward packet to next hop toward original sender node destination
                # specified
            elif pkt_type == 7:
                seq, src, dst, dstcentroid = read_data_unicast_ack(packet)
                # Forward packet to next hop toward centroid destination specified. If
                # centroid, wait for K such packets and transmit
                # DATA_MULTICAST_ACK toward original sender node
            else:
                print('Unknown packet type')


routetable = {"S": ['192.168.1.0']}

if __name__ == '__main__':
    print('router started')
    udp_router = udprouter(id=201, port=8881, rt=routetable)
    udp_router.handle_packets()
