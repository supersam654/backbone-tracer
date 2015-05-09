#!/usr/bin/python
# python main.py GeoLite2-City-CSV_20150505/GeoLite2-City-Blocks-IPv4.csv
"""
Python traceroute tool.

Script used in the internet mapping project.
Fun fact: I decided not to reimplement traceroute functionality.
"""

from traceroute import traceroute, Trace
from writers import *
import logging
import ipgetter
from netaddr import IPNetwork
from sys import argv
import csv
from threading import Thread, Lock

logger = logging.getLogger('backbone-tracer')

def get_ip_from_range(ip_range):
    ip = IPNetwork(ip_range).ip
    return ip + 1

def skip_beginning(itr, offset):
    for i in range(offset):
        itr.next()
    return itr

def compute_trace(source, row):
    destination = get_ip_from_range(row['network'])
    logging.info("Tracerouting: %s" % destination)
    output = traceroute(source, str(destination))
    output.latitude = row['latitude']
    output.longitude = row['longitude']
    return output

def write_trace(order, output):
    if not writer.write(order, output.__dict__):
        logger.warning("Failed to write %s" % output.__dict__)

def tracer(source, itr):
    for i, row in itr:
        trace = compute_trace(source, row)
        write_trace(i, trace)

def generate_data(traceroute, input_filename, writer):
    logger.info('Backbone Tracer is tracing IPs..')
    source = ipgetter.myip()
    logger.info('My IP address is: %s' % source)
    with open(input_filename) as csvfile:
        reader = csv.DictReader(csvfile)
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
    filename = argv[1]
    writer = JsonWriter("data.json")
    generate_data(traceroute, filename, writer)
    
            
