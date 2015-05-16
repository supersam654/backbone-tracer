#!/usr/local/bin/python -u

import json
import sys
import gzip
import struct

def to_bin(trace):
    source = trace['source']
    destination = trace['destination']
    oneDimension = []
    for hop in trace['hops']:
        oneDimension.extend(hop)
    format_str = 'LL' + 'HLI' * len(trace['hops'])
    format_length = struct.calcsize(format_str)
    return struct.pack('<H' + format_str, format_length, source, destination, *oneDimension)

counter = 0
with gzip.open("data/trace.json.gz") as in_file:
    with open("data/trace.bin", "wb") as out_file:
        sys.stdout.write("Converting old data to a binary format")
        for line in in_file:
            if counter % 1e5 == 0:
                sys.stdout.write('.')
            counter += 1
            trace = json.loads(line)
            binary = to_bin(trace)
            out_file.write(binary)

print("\nAll Done!")
# I'm far to lazy to call it from python, but you have to run
# `7z a data/trace.bin/7z data/trace.bin;rm data/trace.json.gz` now.
