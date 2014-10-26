#!/usr/bin/python

import time

from socket          import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, gethostbyname
from lockdown.common import read_json

def test(dest, port):
    x = socket(family=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP)
    b = time.time()
    x.connect((dest, port))
    a = time.time()
    x.close()
    return a-b

def run_tests(dst_file):
    results    = []
    test_cases = read_json(dst_file)

    for case in test_cases.get('hosts'):
        ( url, port, runs ) = ( case.get('url'), case.get('port'), case.get('runs') )

        ip = gethostbyname(url)
        ( total, highest, lowest )  = ( 0, 0, 1000 )

        for run in range(0, runs):
            result = test(ip, port)
            total += result
            if result > highest:
                highest = result

            if result < lowest:
                lowest  = result

        results.append(PerformanceResult(url, total/runs, highest, lowest))

    return results

class PerformanceResult:

    def __init__(self, url, avg, max, min):
        self.url = url
        self.avg = avg
        self.max = max
        self.min = min
