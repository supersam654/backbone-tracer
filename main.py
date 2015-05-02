#!/usr/bin/python
"""
Python traceroute tool.

Script used in the internet mapping project.
Fun fact: I decided not to reimplement traceroute functionality.
"""

from random import randint
from traceroute import traceroute
from writers import *
import struct
import logging

def calc_format_string(size):
    return "<L" + "Li" * ((size - 4) / 8)

def read_data():
    with open(FILENAME, "rb") as f:
        while True:
            size = f.read(1)
            if not size: break
            size = struct.unpack("<B", size)[0]
            trace = f.read(size)
            data = struct.unpack(calc_format_string(size), trace)
            print data

def generate_data(traceroute, writer):
    logger = logging.getLogger('backbone-tracer')
    logger.info('Backbone Tracer is tracing IPs..')
    while True:
        ip = randint(0, 2**32 - 1)
        logger.info("Tracerouting: %d" % ip)
        try:
            output = traceroute(ip)
            if not writer.write(output):
                logger.info("Failed to write %d" % output)
        except ValueError, e:
            logger.warning(e)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_data(traceroute, FileWriter("output.bin"))
    read_data()