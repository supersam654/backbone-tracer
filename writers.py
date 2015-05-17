import json
from threading import Lock
import struct

def _to_bin(trace):
    source = trace['source']
    destination = trace['destination']
    oneDimension = []
    for hop in trace['hops']:
        count, ip, time = hop
        oneDimension.extend([ip, count, time])
    format_str = 'QQ' + 'QII' * len(trace['hops'])
    format_length = struct.calcsize(format_str)
    return struct.pack('<Q' + format_str, format_length, source, destination, *oneDimension)

class Writer(object):
    def __init__(self, filename):
        self.filename = filename
        self.next_to_write = 0
        self.waiting = {}
        self.lock = Lock()

    def _queue(self, i, trace):
        self.waiting[i] = trace

    def _write_queue(self):
        with self.lock:
            with open(self.filename, "ab") as f:
                while self.waiting.has_key(self.next_to_write):
                    trace = self.waiting[self.next_to_write]
                    data = _to_bin(trace)
                    f.write(data)
                    del self.waiting[self.next_to_write]
                    self.next_to_write += 1

    def write(self, order, trace):
        if not trace:
            return False
        self._queue(order, trace.__dict__)
        self._write_queue()
        return True

    def count(self):
        try:
            with open(self.filename) as f:
                return sum (1 for line in f)
        except IOError:
            return 0

