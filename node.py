from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from packets import *


class client:
    def __init__(self, id, ip, gateway, port):
        self.ip = ip
        self.id = id
        self.default_gateway = gateway
        self.port = port

    def send_packet(self, packet, dst):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        print(packet)
        s.sendto(packet, dst)
        print('Sent packet type ' + str(packet[1]) + ' to ' + str(dst))
        s.close()
        return 0

    def listen(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('0.0.0.0', self.port))
        while True:
            packet, addr = s.recvfrom(1024)
            print('Recieved from:', addr)
            pkt_type = packet[1]
            if pkt_type == 1:
                seq, ttl, src = read_hello(packet)
                print(src)
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
    node = client(id=101, ip='192.168.0.5', gateway=('192.168.0.0', 8881), port=8881)
    hello = create_hello(1, 10, 1)
    node.send_packet(hello, ('192.0.0.0', 8881))
    node.listen()
