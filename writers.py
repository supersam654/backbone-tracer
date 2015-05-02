import struct

class Writer(object):
    def write(self, normalized_traceroute_output):
        raise NotImplementedError("Use a concrete writer!")

def to_bin(trace):
    destination_ip, hops = trace
    oneDimension = []
    for hop in hops:
        oneDimension.extend(hop)
    format_str = 'L' + 'Li' * (len(oneDimension) / 2)
    format_length = struct.calcsize(format_str)
    return struct.pack('<B' + format_str, format_length, destination_ip, *oneDimension)

class FileWriter(Writer):
    def __init__(self, filename):
        self.filename = filename

    def write(self, normalized_traceroute_output):
        if not normalized_traceroute_output:
            return False
        data = to_bin(normalized_traceroute_output)
        with open(self.filename, "ab") as f:
            f.write(data)

