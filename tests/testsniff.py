#!/usr/bin/env python

import getopt
import sys

import dpkt
import pcap


def usage():
    print >>sys.stderr, 'Usage: %s [-i device] [pattern]' % sys.argv[0]
    devs = pcap.findalldevs()
    print >>sys.stderr, '\nAvailable devices:\n\t', '\n\t'.join(devs)
    sys.exit(1)


def main():
    opts, args = getopt.getopt(sys.argv[1:], 'i:h')
    name = None
    for o, a in opts:
        if o == '-i':
            name = a
        else:
            usage()

    pc = pcap.pcap(name, timeout_ms=50)
    pc.setfilter(' '.join(args))
    decode = {
        pcap.DLT_LOOP: dpkt.loopback.Loopback,
        pcap.DLT_NULL: dpkt.loopback.Loopback,
        pcap.DLT_EN10MB: dpkt.ethernet.Ethernet
    }[pc.datalink()]

    try:
        print 'listening on %s: %s' % (pc.name, pc.filter)
        for ts, pkt in pc:
            print ts, repr(decode(pkt))
    except KeyboardInterrupt:
        nrecv, ndrop, nifdrop = pc.stats()
        print '\n%d packets received by filter' % nrecv
        print '%d packets dropped by kernel' % ndrop

if __name__ == '__main__':
    main()
