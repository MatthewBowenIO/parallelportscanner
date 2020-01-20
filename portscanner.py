#!/usr/bin/env python
from socket import *
from netaddr import *

from joblib import Parallel, delayed
import multiprocessing
import time, datetime
import argparse

def parallel_port_scan(cc, ip, portStart, portEnd):
    return Parallel(n_jobs = cc)(delayed(port_scan)(ip, i) for i in range(portStart, portEnd))

def port_scan(ip, port):
    print("{}: {}".format(str(ip), port))
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(.5)
    try:
        with open("logs.txt", "a") as log:
            if port == 21:
                log.write("Last IP Scanned: {}\n".format(ip))            
            s = s.connect((str(ip), port))
            log.write("{}: Port open: {}\n".format(ip, port))
            log.close()

        print("{}: Port open: {}".format(ip, port))
    except Exception as e:
        print(e)
        last_ip = str(ip)
        pass

def main():
    cc = multiprocessing.cpu_count()

    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--ipRange', help = 'IP Range (format: IP-IP', required = True)
    parser.add_argument('-port', '--portRange', help = 'Port Range (format: Port-Port)', required = True)
    args = parser.parse_args()

    ipStart, ipEnd = args.ipRange.split("-")
    portStart, portEnd = args.portRange.split("-")

    print(ipStart, ipEnd, portStart, portEnd)

    ipRange = IPRange(ipStart, ipEnd)

    start = time.time()
    for ip in ipRange:
        last_ip = ip
        parallel_port_scan(cc, ip, int(portStart), int(portEnd))
        #for port in range(int(portStart), int(portEnd)):
            #port_scan(ip, port)
    print(str(datetime.timedelta(seconds=int(time.time() - start))))

if __name__ == "__main__":
    main()