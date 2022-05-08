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
            elif pkt_type == 2:
                seq, src, n, k, ln, dests = read_data_multicast_header(packet)
                data = read_data_multicast_data(packet)
            elif pkt_type == 3:
                seq, src, n, dests = read_centroid_request(packet)
            elif pkt_type == 4:
                seq, src, mean_dist = read_centroid_reply(packet)
            elif pkt_type == 5:
                seq, src, srccentroid, dst = read_data_unicast_header(packet)
                data = read_data_unicast_data(packet)
            elif pkt_type == 6:
                seq, src, dst = read_data_multicast_ack(packet)
            elif pkt_type == 7:
                seq, src, dst, dstcentroid = read_data_unicast_ack(packet)
            else:
                print('Unknown packet type')


if __name__ == '__main__':
    print('router started')
    udp_router = udprouter(id=201, port=8881)
    udp_router.handle_packets()
