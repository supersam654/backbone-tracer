#!/usr/bin/python
"""
Python traceroute tool.

Script used in the internet mapping project.
Fun fact: I decided not to reimplement traceroute functionality.
"""
FILENAME = "output.bin"

from subprocess import check_output
from sys import platform
from random import randint
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

def dotted_quad_to_int(ip):
    parts = ip.split('.')
    i1 = int(parts[0]) << 24
    i2 = int(parts[1]) << 16
    i3 = int(parts[2]) << 8
    i4 = int(parts[3]) << 0
    return i1 + i2 + i3 + i4

def linux_parser(output):
    if "!" in output:
        return None
    data = []
    for line in output.split('\n')[1:]:
        line = line.strip().replace('  ', ' ')
        if line == '':
            continue
        try:
            hop, ip, time, unit = line.split()
            ip = dotted_quad_to_int(ip)
            time = int(float(time) * 1000)
        except ValueError:
            try:
                hop, star = line.split()
                ip = 0
                time = 0
            except ValueError, e:
                print e
                print("Could not interpret this output: %r of %r" % (line, output))
                return None
        # ip is an integer and time is an integer number of microseconds (um = ms * 1000)
        data.append([ip, time])
    return data
    
def osx_parser(output):
    raise NotImplementedError

def win_parser(output):
    raise NotImplementedError

if platform.startswith("linux"):
    TRACEROUTE = ["sudo", "traceroute", "-n", "-I", "-w", "1", "-q", "1", "-m", "20"]
    PARSER = linux_parser
elif platform.startswith("win"):
    raise NotImplementedError("Windows is not supported (yet).")
elif platform.startswith("darwin"):
    TRACEROUTE = ["traceroute", "-P", "ICMP"]
    PARSER = osx_parser
else:
    raise NotImplementedError("Sorry, we haven't implemented this for your OS yet: " + platform)

def to_bin(trace):
    destination_ip, hops = trace
    oneDimension = []
    for hop in hops:
        oneDimension.extend(hop)
    format_str = 'L' + 'Li' * (len(oneDimension) / 2)
    format_length = struct.calcsize(format_str)
    return struct.pack('<B' + format_str, format_length, destination_ip, *oneDimension)

def traceroute(ip):
    output = check_output(TRACEROUTE + [str(ip)])
    parsed_output = PARSER(output)
    if not parsed_output:
        return None
    else:
        return to_bin((ip, parsed_output))

def generate_data():
    with open(FILENAME, "ab") as f:
        while True:
            ip = randint(0, 2**32 - 1)
            output = traceroute(ip)
            if output:
                f.write(output)
                print output

if __name__ == "__main__":
    #generate_data()
    read_data()