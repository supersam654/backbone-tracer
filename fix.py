#!/usr/local/bin/python -u

import json
import sys
import gzip
from netaddr import IPAddress

counter = 0
with gzip.open("data/trace.json.gz") as in_file:
    with open("data/out.json", "w") as out_file:
        sys.stdout.write("Converting old data to an even less verbose format")
        for line in in_file:
            if counter % 1e5 == 0:
                sys.stdout.write('.')
            counter += 1
            trace = json.loads(line)
            keep = {}
            keep['source'] = int(IPAddress(trace['source']))
            keep['destination'] = int(IPAddress(trace['destination']))
            keep['hops'] = [[count, int(IPAddress(ip)), time] for count, ip, time in trace['hops']]
            s = json.dumps(keep)
            out_file.write(s + "\n")
print("\nAll Done!")
# I'm far to lazy to call it from python, but you have to run
# `rm data/trace.json.gz; gzip data/out.json; mv data/out.json.gz data/trace.json.gz` now.