#!/usr/bin/python
"""
Usage: scantcp.py [OPTIONS]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
                        filename to read [default: hosts]
  -c, --closed          Print only closed connections [default: False]
  -o, --open            Print only open connections [default: False]
  -u, --unresoved       Print only open connections [default: False]

Config file example: serverlist
192.168.1.2 server1 tcp 22
192.168.1.3 server2 tcp 22,88
192.168.1.4 server3 udp 53
192.168.1.5 server4 udp 53,161
"""

import socket
from optparse import OptionParser
import sys

TCP_PORT = 22
BUFFER_SIZE = 1024
MESSAGE = "ping"

PARSER = OptionParser()
PARSER.add_option(
    "-f", "--file",
    dest="filename",
    default="hosts",
    help="filename to read [default: %default]"
    )
PARSER.add_option(
    "-c",
    "--closed",
    action="store_true",
    dest="closedses",
    default=False,
    help="Print only closed connections [default: %default]"
    )
PARSER.add_option(
    "-o",
    "--open",
    action="store_true",
    dest="openses", default=False,
    help="Print only open connections [default: %default]"
    )
PARSER.add_option(
    "-u",
    "--unresoved",
    action="store_true",
    dest="unresolved",
    default=False,
    help="Print only open connections [default: %default]"
    )
(OPTIONS, ARGS) = PARSER.parse_args()

UNRCNT = 0
OPNCNT = 0
CLSCNT = 0

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    with open(OPTIONS.filename) as f:
        for line in f:
            if line.strip() == "":
                continue
            len_line_strip = len(line.strip())
            if len_line_strip == 0:
                continue
            result = ""
            new_line = line.strip()
            TCP_IP, HSTNAME, TCP_UDP, TCP_PORTS = new_line.split(" ")
            TCP_PORT_L = TCP_PORTS.split(",")
            for TCP_PORT in TCP_PORT_L:
                if TCP_UDP == 'tcp':
                    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                elif TCP_UDP == 'udp':
                    S = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                else:
                    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                S.settimeout(3)
                try:
                    result = S.connect_ex((HSTNAME, int(TCP_PORT)))
                    try:
                        ADDR = socket.gethostbyname(TCP_IP)
                    except socket.error:
                        print "Server " + TCP_IP + " connect error"
                    if result == 0:
                        OPNCNT += 1
                        if OPTIONS.openses:
                            print str("\r" + ADDR +
                                      " - " + HSTNAME +
                                      " - " + TCP_IP +
                                      " Port " + TCP_UDP +
                                      "/" + str(TCP_PORT) +
                                      " open" +
                                      " - " + str(ADDR == TCP_IP)
                                     )
                    else:
                        CLSCNT += 1
                        if OPTIONS.closedses:
                            print str("\r" + ADDR +
                                      " - " + HSTNAME +
                                      " - " + TCP_IP +
                                      " Port " + TCP_UDP +
                                      "/" + str(TCP_PORT) +
                                      " closed" +
                                      " - " + str(ADDR == TCP_IP)
                                     )
                except socket.gaierror:
                    if OPTIONS.unresolved:
                        print 'Hostname could not be resolved. Exiting ' + TCP_IP + " - " + HSTNAME
                    UNRCNT += 1

except KeyboardInterrupt:
    print "You pressed Ctrl+C"
    sys.exit()

except IOError as scioer:
    if scioer.errno == 2:
        print "No configuartion or host file specified"
        print "-f FILENAME, --file=FILENAME"
        sys.exit()

print "Host names and or ports un-resolved: ".ljust(39) + str(UNRCNT)
print "Hosts on port reachable: ".ljust(39) + str(OPNCNT)
print "Hosts on port not reachable: ".ljust(39) + str(CLSCNT)
print "Total of Hosts on ports checked: ".ljust(39) + str(UNRCNT + OPNCNT + CLSCNT)
