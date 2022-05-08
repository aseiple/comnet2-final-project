import struct


# Hello PKT
# Type (1 BYTE) := 1
# SEQ (1 BYTE)
# TTL (1 BYTE)
# SRC (1 BYTE)
def create_hello(seq, ttl, src):
    header = struct.pack('BBBB', '1', seq, ttl, src)
    return header


def read_hello(pkt):
    header = pkt[1:]
    seq, ttl, src = struct.unpack('BBB', header)
    return seq, ttl, src


# Data Multicast PKT
# TYPE (1 BYTE) := 2
# SEQ (1 BYTE)
# SRC (1 BYTE)
# N (1 BYTE)
# K (1 BYTE)
# LEN (1 BYTE)
# DESTINATIONS (1 BYTE)
# DATA (<= 1000 BYTES)
def create_data_multicast(seq, src, n, k, dsts, data):
    ln = len(data)
    header = struct.pack('BBBBBBB', '2', seq, src, n, k, ln, dsts)
    return header + bytes(data, 'utf-8')


def read_data_multicast_header(pkt):
    header = pkt[1:7]
    seq, src, n, k, ln, dsts = struct.unpack('BBBBBB', header)
    return seq, src, n, k, ln, dsts


def read_data_multicast_data(pkt):
    data = pkt[8:]
    return data


# Centroid Request PKT
# TYPE (1 BYTE) := 3
# SEQ (1 BYTE)
# SRC (1 BYTE)
# N (1 BYTE)
# DESTINATIONS (1 BYTE)
def create_centroid_request(seq, src, n, dsts):
    header = struct.pack('BBBBB', '3', seq, src, n, dsts)
    return header


def read_centroid_request(pkt):
    header = pkt[1:]
    seq, src, n, dsts = struct.unpack('BBBB', header)
    return seq, src, n, dsts


# Centroid Reply PKT
# TYPE (1 BYTE) := 4
# SEQ (1 BYTE)
# SRC (1 BYTE)
# MEAN DISTANCE (1 BYTE)
def create_centroid_reply(seq, src, meandist):
    header = struct.pack('BBBB', '4', seq, src, meandist)
    return header


def read_centroid_reply(pkt):
    header = pkt[1:]
    seq, src, meandist = struct.unpack('BBB', header)
    return seq, src, meandist


# Data Unicast PKT
# TYPE (1 BYTE) := 5
# SEQ (1 BYTE)
# SRC (1 BYTE)
# SRC CENTROID (1 BYTE)
# DEST (1 BYTE)
# DATA (<= 1000 BYTES)
def create_data_unicast(seq, src, srccentroid, dst):
    header = struct.pack('BBBBB', '5', seq, src, srccentroid, dst)
    return header


def read_data_unicast_header(pkt):
    header = pkt[1:5]
    seq, src, srccentroid, dst = struct.unpack('BBBB', header)
    return seq, src, srccentroid, dst


def read_data_unicast_data(pkt):
    data = pkt[6:]
    return data


# Data Multicast ACK PKT
# TYPE (1 BYTE) := 6
# SEQ (1 BYTE)
# SRC (1 BYTE)
# DEST (1 BYTE)
def create_data_multicast_ack(seq, src, dst):
    header = struct.pack('BBBB', '6', seq, src, dst)
    return header


def read_data_multicast_ack(pkt):
    header = pkt[1:]
    seq, src, dst = struct.unpack('BBB', header)
    return seq, src, dst


# Data Unicast ACK PKT
# TYPE (1 BYTE) := 7
# SEQ (1 BYTE)
# SRC (1 BYTE)
# DEST (1 BYTE)
# DEST CENTROID (1 BYTE)
def create_data_unicast_ack(seq, src, dst, dst_centroid):
    header = struct.pack('BBBBB', '7', seq, src, dst, dst_centroid)
    return header


def read_data_unicast_ack(pkt):
    header = pkt[1:]
    seq, src, dst, dst_centroid = struct.unpack('BBBB', header)
    return seq, src, dst, dst_centroid
