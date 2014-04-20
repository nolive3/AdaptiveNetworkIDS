#!/usr/bin/env python
#
# Author: Arn Vollebregt
# Version: 1.0
# Release date: 26-05-2010
#
# This script provides a Unix Domain Socket server, which processes Alertpkt's
# provided by Snort when unsock logging is enabled.
#
# Release notes:
# v1.0 (26-05-2010)
#  - Initial release
#
# TODO:
#  - Parse raw packet data (perhaps with one of the PCAP modules?)

import os
import socket
import ctypes

class packet(ctypes.Structure):
    _fields_ = [
        ("dstMac", ctypes.c_ubyte * 6),
        ("srcMac", ctypes.c_ubyte * 6),
    ]

    def __repr__(self):
        return ("<Alertpkt(msg=%s, pkth=%s, dlthdr=%i, nethdr=%i, transhdr=%i, datasize=%i, val=%i, event=%s)>") % ( #pkt=<%s>,
            ctypes.string_at(self.alertmsg),
            self.pkth
        )

    def __str__(self):return self.__repr__()

# time.h:15
class timeval(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_long),
        ("tv_usec", ctypes.c_long)
    ]

    def __repr__(self):
        return ("<timeval(tv_sec=%i, tv_usec=%i)>") % (
            self.tv_sec,
            self.tv_usec
        )

    def __str__(self):return self.__repr__()

# pcap.h:154
class pcap_pkthdr(ctypes.Structure):
    _fields_ = [
        ("ts", timeval),
        ("caplen", ctypes.c_uint, 32),
        ("len", ctypes.c_uint, 32)
    ]

    def __repr__(self):
        return ("<pcap_pkthdr(ts=%s, caplen=%i, len=%i)>") % (
            self.ts,
            self.caplen,
            self.len
        )

    def __str__(self):return self.__repr__()

# pcap_pkthdr32.h:43
class sf_timeval32(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_uint, 32),
        ("tv_usec", ctypes.c_uint, 32)
    ]

    def __repr__(self):
        return ("<sf_timeval32(tv_sec=%i, tv_usec=%i)>") % (
            self.tv_sec,
            self.tv_usec
        )

    def __str__(self):return self.__repr__()

# If you dont get the expected content (or content with a weird offset) in
# Event objects, try changing SNAPLEN used in Alertpkt.
# event.h:41
class Event(ctypes.Structure):
    _fields_ = [
        ("sig_generator", ctypes.c_uint, 32),
        ("sig_id", ctypes.c_uint, 32),
        ("sig_rev", ctypes.c_uint, 32),
        ("classification", ctypes.c_uint, 32),
        ("priority", ctypes.c_uint, 32),
        ("event_id", ctypes.c_uint, 32),
        ("event_reference", ctypes.c_uint, 32),
        ("ref_time", sf_timeval32)
    ]

    def __repr__(self):
        return ("<Event(sig_generator=%i, sig_id=%i, sig_rev=%i, classification=%i, priority=%i, event_id=%i, event_reference=%i, ref_time=%s)>") % (
            self.sig_generator,
            self.sig_id,
            self.sig_rev,
            self.classification,
            self.priority,
            self.event_id,
            self.event_reference,
            self.ref_time
        )

    def __str__(self):return self.__repr__()

ALERTMSG_LENGTH = 256 # decode.h:1754
SNAPLEN = 1514 # decode.h:340
# Weird enough, Ubuntu compiles with 1514, and not 1500 
#SNAPLEN = 1500 # decode.h:342

# spo_alert_unixsock.h:37
class Alertpkt(ctypes.Structure):
    _fields_ = [
        ("alertmsg", ctypes.c_ubyte * ALERTMSG_LENGTH),
        ("pkth", pcap_pkthdr),
        ("dlthdr", ctypes.c_uint, 32),
        ("nethdr", ctypes.c_uint, 32),
        ("transhdr", ctypes.c_uint, 32),
        ("data", ctypes.c_uint, 32),
        ("val", ctypes.c_uint, 32),
        ("pkt", ctypes.c_ubyte * SNAPLEN),
        ("event", Event),
    ]

    def __repr__(self):
        return ("<Alertpkt(msg=%s, pkth=%s, dlthdr=%i, nethdr=%i, transhdr=%i, datasize=%i, val=%i, pkt=<%s>, event=%s)>") % ( #pkt=<%s>,
            ctypes.string_at(self.alertmsg),
            self.pkth,
            self.dlthdr,
            self.nethdr,
            self.transhdr,
            self.data,
            self.val,
            ctypes.string_at(self.pkt),#{0:"PACKET_STRUCT",1:"NOPACKET_STRUCT",2:"NO_TRANSHDR"}[self.val],
            self.event
        )

    def __str__(self):return self.__repr__()

if __name__ == "__main__":
    # spo_alert_unixsock.c:59
    UNSOCK_FILE = "snort_alert"
    fd = ("/var/log/snort/snort_alert")
    server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    if os.path.exists(fd):
        os.remove(fd)

    try:
        server.bind(fd)
    except:
        print sys.exc_info()
        sys.exit(1)

    while 1:
        data = server.recv(2048)
        #print data
        alertpkt = Alertpkt()
        size = min(len(data), ctypes.sizeof(alertpkt))
        ctypes.memmove(ctypes.addressof(alertpkt), data, size)
        print alertpkt
        if not data: break

    server.close()
