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

def generate_data(traceroute, input_filename, writer):
    logger = logging.getLogger('backbone-tracer')
    logger.info('Backbone Tracer is tracing IPs..')
    source = ipgetter.myip()
    logger.info('My IP address is: %s' % source)
    with open(input_filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            destination = IPNetwork(row['network']).ip + 1
            logger.info("Tracerouting: %s" % destination)
            try:
                output = traceroute(source, str(destination))
                output.latitude = row['latitude']
                output.longitude = row['longitude']
                if not writer.write(output.__dict__):
                    logger.info("Failed to write %s" % output.__dict__)
            except ValueError, e:
                logger.warning(e)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    filename = argv[1]
    writer = JsonWriter("data.json")
    generate_data(traceroute, filename, writer)
    
            
