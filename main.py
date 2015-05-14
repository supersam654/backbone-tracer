#!/usr/bin/python
# python main.py GeoLite2-City-CSV_20150505/GeoLite2-City-Blocks-IPv4.csv
"""
Python traceroute tool.

Script used in the internet mapping project.
Fun fact: I decided not to reimplement traceroute functionality.
"""

from traceroute import traceroute
from writers import *
import logging
import ipgetter
import gzip
from threading import Thread

IN_FILENAME = 'data/ips.txt.gz'
OUT_FILENAME = 'data/data.json'

logger = logging.getLogger('backbone-tracer')

def skip_beginning(itr, offset):
    for i in range(offset):
        itr.next()
    return itr

def compute_trace(source, destination):
    logging.info("Tracerouting: %s" % destination)
    output = traceroute(source, str(destination))
    return output

def tracer(source, itr):
    for i, ip in itr:
        trace = compute_trace(source, ip)
        writer.write(i, output)

def generate_data(traceroute, writer):
    logger.info('Backbone Tracer is tracing IPs..')
    source = ipgetter.myip()
    logger.info('My IP address is: %s' % source)
    with gzip.open(IN_FILENAME) as reader:
        offset = writer.count()
        itr = enumerate(skip_beginning(reader, offset))
        logger.info("Skipping past the first %d addresses." % offset)
        threads = []
        for i in range(10):
            thread = Thread(target=tracer, args=(source, itr))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    writer = JsonWriter(OUT_FILENAME)
    generate_data(traceroute, writer)
