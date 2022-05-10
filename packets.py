import struct
from routingtable import *

# Hello PKT
# Type (1 BYTE) := 1
# SEQ (1 BYTE)
# TTL (1 BYTE)
# SRC (1 BYTE)
def create_hello(seq, ttl, src):
    header = struct.pack('BBBB', 1, seq, ttl, src)
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
    if len(dsts) == 1:
        header = struct.pack('BBBBBBB', 2, seq, src, n, k, len(data), dsts[0])
    elif len(dsts) == 2:
        header = struct.pack('BBBBBBBB', 2, seq, src, n, k, len(data), dsts[0], dsts[1])
    elif len(dsts) == 3:
        header = struct.pack('BBBBBBBBB', 2, seq, src, n, k, len(data), dsts[0], dsts[1], dsts[2])
    ln = len(data)

    return header + bytes(data, 'utf-8')


def read_data_multicast_header(pkt):
    seq, src, n, k, ln = struct.unpack('BBBBB', pkt[1:6])
    if n == 1:
        dsts = pkt[6]
        return seq, src, n, k, ln, dsts
    elif n == 2:
        dsts1, dsts2 = struct.unpack('BB', pkt[6:8])
        return seq, src, n, k, ln, (dsts1, dsts2)
    elif n == 3:
        dsts1, dsts2, dsts3 = struct.unpack('BBB', pkt[6:9])
        return seq, src, n, k, ln, (dsts1, dsts2, dsts3)
    return


def read_data_multicast_data(pkt):
    data = pkt[9:]
    return data.decode("utf-8")


# Centroid Request PKT
# TYPE (1 BYTE) := 3
# SEQ (1 BYTE)
# SRC (1 BYTE)
# N (1 BYTE)
# DESTINATIONS (1 BYTE)
def create_centroid_request(seq, src, n, dsts):
    print(seq, src, n, dsts)
    if len(dsts) == 1:
        header = struct.pack('BBBBB', 3, seq, src, n, dsts[0])
        return header
    elif len(dsts) == 2:
        header = struct.pack('BBBBBB', 3, seq, src, n, dsts[0], dsts[1])
        return header
    elif len(dsts) == 3:
        header = struct.pack('BBBBBBB', 3, seq, src, n, dsts[0], dsts[1], dsts[2])
        return header
    return


def read_centroid_request(pkt):
    seq, src, n = struct.unpack('BBB', pkt[1:4])
    if n == 1:
        dsts = pkt[4]
        return seq, src, n, dsts
    elif n == 2:
        dsts1, dsts2 = struct.unpack('BB', pkt[4:6])
        return  seq, src, n, (dsts1, dsts2)
    elif n == 3:
        dsts1, dsts2, dsts3 = struct.unpack('BBB', pkt[4:7])
        return seq, src, n, (dsts1, dsts2, dsts3)
    return


# Centroid Reply PKT
# TYPE (1 BYTE) := 4
# SEQ (1 BYTE)
# SRC (1 BYTE)
# MEAN DISTANCE (1 BYTE)
def create_centroid_reply(seq, src, meandist):
    header = struct.pack('BBBB', 4, seq, src, meandist)
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
def create_data_unicast(seq, src, srccentroid, dst, data):
    header = struct.pack('BBBBB', 5, seq, src, srccentroid, dst)
    return header + bytes(data, 'utf-8')


def read_data_unicast_header(pkt):
    header = pkt[1:5]
    seq, src, srccentroid, dst = struct.unpack('BBBB', header)
    return seq, src, srccentroid, dst


def read_data_unicast_data(pkt):
    data = pkt[5:]
    return data.decode("utf-8")


# Data Multicast ACK PKT
# TYPE (1 BYTE) := 6
# SEQ (1 BYTE)
# SRC (1 BYTE)
# DEST (1 BYTE)
def create_data_multicast_ack(seq, src, dst):
    header = struct.pack('BBBB', 6, seq, src, dst)
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
    header = struct.pack('BBBBB', 7, seq, src, dst, dst_centroid)
    return header


def read_data_unicast_ack(pkt):
    header = pkt[1:]
    seq, src, dst, dst_centroid = struct.unpack('BBBB', header)
    return seq, src, dst, dst_centroid
