#!/usr/bin/env python
from socket import *
from netaddr import *

from joblib import Parallel, delayed
import multiprocessing
import time, datetime
import argparse

def parallel_port_scan(cc, ip, port):
    return Parallel(n_jobs = cc)(delayed(port_scan)(ip, i) for i in range(port))

def port_scan(ip, port):
    print "{}: {}".format(ip, port)
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s = s.connect(ip, port)

        with open("logs.txt", "w") as log:
            log.write("{}: Port open: {}\n".format(ip, port))
            log.close()

        print "{}: Port open: {}".format(ip, port)
    except Exception as e:
        pass

def main():
    cc = multiprocessing.cpu_count()

    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--ipRange', help = 'IP Range (format: IP-IP', required = True)
    parser.add_argument('-port', '--portRange', help = 'Port Range (format: Port-Port)', required = True)
    args = parser.parse_args()

    ipStart, ipEnd = args.ipRange.split("-")
    portStart, portEnd = args.portRange.split("-")

    print ipStart, ipEnd, portStart, portEnd

    ipRange = IPRange(ipStart, ipEnd)

    start = time.time()
    for ip in ipRange:
        parallel_port_scan(cc, ip, int(portEnd))
        #for port in range(int(portStart), int(portEnd)):
            #port_scan(ip, port)
    print str(datetime.timedelta(seconds=int(time.time() - start)))

if __name__ == "__main__":
    main()