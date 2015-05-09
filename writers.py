import json

class Writer(object):
    def write(self, trace):
        raise NotImplementedError("Use a concrete writer!")

    def count(self):
        raise NotImplemenetedError("Use a concrete writer!")

class JsonWriter(Writer):
    def __init__(self, filename):
        self.filename = filename

    def write(self, trace):
        if not trace:
            return False
        with open(self.filename, "a") as f:
            s = json.dumps(trace)
            f.write(s + '\n')
        return True

    def count(self):
        with open(self.filename) as f:
            return sum (1 for line in f)

