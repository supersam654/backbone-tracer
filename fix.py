#!/usr/local/bin/python -u

import json
import sys

counter = 0
with open("data/data.json") as in_file:
    with open("data/out.json", "w") as out_file:
        sys.stdout.write("Converting old data to a less verbose format")
        for line in in_file:
            if counter % 1e5 == 0:
                sys.stdout.write('.')
            counter += 1
            trace = json.loads(line)
            keep = {}
            keep['source'] = trace['source']
            keep['destination'] = trace['destination']
            keep['hops'] = trace['hops']
            s = json.dumps(keep)
            out_file.write(s + "\n")
print("\nAll Done!")
# I'm far to lazy to call it from python, but you have to run
# `gzip data/out.json; mv data/out.json.gz data/trace.json.gz` now.