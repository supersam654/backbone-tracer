#!/usr/bin/python
"""
This file contains different methods for running the traceroute command and getting normalized output out of it.

Currently only tested on linux but stubbed out support for Windows and OSX.
"""

from subprocess import check_output
from sys import platform

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

def linux_traceroute(ip):
    CMD = ["sudo", "traceroute", "-n", "-I", "-w", "1", "-q", "1", "-m", "20"] + [str(ip)]
    output = chceck_output(CMD)
    parsed_output = linux_parser(output)
    if not parsed_output:
        return None
    else:
        return (ip, parsed_output)

if platform.startswith("linux"):
    traceroute = linux_traceroute
elif platform.startswith("win"):
    raise NotImplementedError("Windows is not supported (yet).")
    # traceroute = windows_traceroute
elif platform.startswith("darwin"):
    raise NotImplementedError("OSX is not supported (yet).")
    # traceroute = osx_traceroute
else:
    raise NotImplementedError("Sorry, we haven't implemented this for your OS yet: " + platform)
