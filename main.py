#!/usr/bin/python
"""
Python traceroute tool.

Script used in the internet mapping project.
Fun fact: I decided not to reimplement traceroute functionality.
"""

from random import randint
from parsers import traceroute
from writers import *
import struct

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
    while True:
        ip = randint(0, 2**32 - 1)
        print "Tracerouting: %d" % ip
        output = traceroute(ip)
        writer.write(output)

if __name__ == "__main__":
    generate_data(traceroute, FileWriter("output.bin"))
    read_data()