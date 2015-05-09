#!/usr/bin/python
"""
This file contains different methods for running the traceroute command and getting normalized output out of it.

Currently only tested on linux but stubbed out support for Windows and OSX.
"""

from subprocess import check_output
from sys import platform

class Trace(object):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.hops = []
        self.latitude = 9000.1
        self.longitude = 9000.1

    def add_hop(self, ip, microseconds):
        self.hops.append([len(self.hops), ip, microseconds])

def linux_parser(output, source, destination):
    if "!" in output:
        return None
    data = Trace(source, destination)
    for line in output.split('\n')[1:]:
        line = line.strip().replace('  ', ' ')
        if line == '':
            continue
        try:
            hop, ip, time, unit = line.split()
            time = int(float(time) * 1000)
        except ValueError:
            try:
                hop, star = line.split()
                ip = 0
                time = 0
            except ValueError, e:
                raise ValueError("Could not interpret this output: %r of %r" % (line, output))
                return None
        # ip is a string and time is an integer number of microseconds (um = ms * 1000)
        data.add_hop(ip, time)
    return data

def linux_traceroute(source, destination):
    cmd = ["sudo", "traceroute", "-n", "-I", "-w", "1", "-q", "1", "-m", "20"] + [destination]
    output = check_output(cmd)
    trace = linux_parser(output, source, destination)
    if not trace:
        return None
    else:
        return trace

def osx_traceroute(source, destination):
    return linux_traceroute(source, destination)

if platform.startswith("linux"):
    traceroute = linux_traceroute
elif platform.startswith("win"):
    raise NotImplementedError("Windows is not supported (yet).")
    # traceroute = windows_traceroute
elif platform.startswith("darwin"):
    traceroute = osx_traceroute
else:
    raise NotImplementedError("Sorry, we haven't implemented this for your OS yet: " + platform)
