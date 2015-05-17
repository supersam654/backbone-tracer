#!/usr/local/bin/python -u
import json
import sys
import gzip
import struct
from netaddr import IPAddress

def to_bin(trace):
    source = int(IPAddress(trace['source']))
    destination = int(IPAddress(trace['destination']))
    oneDimension = []
    for hop in trace['hops']:
        count, ip, time = hop
        oneDimension.extend([int(IPAddress(ip)), count, time])
    format_str = 'QQ' + 'QII' * len(trace['hops'])
    format_length = len(trace['hops'])
    return struct.pack('<I' + format_str, format_length, source, destination, *oneDimension)

counter = 0
with gzip.open("data/data.json.gz") as in_file:
    with open("data/trace.bin", "wb") as out_file:
        sys.stdout.write("Converting old data to a binary format")
        sys.stdout.flush()
        for line in in_file:
            if counter % 1e5 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()
            counter += 1
            trace = json.loads(line)
            binary = to_bin(trace)
            out_file.write(binary)

print("\nAll Done!")
# I'm far to lazy to call it from python, but you have to run
# `gzip data/trace.bin;rm data/trace.json.gz` now.
