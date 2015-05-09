import json
import gzip

class JsonWriter(object):
    def __init__(self, filename):
        self.filename = filename
        self.next_to_write = 0
        self.waiting = {}

    def _queue(self, i, trace):
        self.waiting[i] = trace

    def _write_queue(self):
        with gzip.open(self.filename, "a") as f:
            while self.waiting.has_key(self.next_to_write):
                trace = self.waiting[self.next_to_write]
                s = json.dumps(trace)
                f.write(s + '\n')
                del self.waiting[self.next_to_write]
                self.next_to_write += 1

    def write(self, order, trace):
        if not trace:
            return False
        self._queue(order, trace)
        self._write_queue()
        return True

    def count(self):
        try:
            with gzip.open(self.filename) as f:
                return sum (1 for line in f)
        except IOError:
            return 0

