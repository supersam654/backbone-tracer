import gzip
from netaddr import IPNetwork
from netaddr.core import AddrFormatError
import sys

_geo_data = {}
with gzip.open('data/geo.txt.gz') as f:
    sys.stdout.write("Reading geo data")
    counter = 0
    for line in f:
        if counter % 1e5 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        counter += 1
        net, latitude, longitude = line.split(' ')
        longitude = longitude[:-1] # Remove trailing newline.
        _geo_data[IPNetwork(net)] = (latitude, longitude)
    print "\nFinished loading geodata!"

def get_geo(ip):
    try:
        # Find the most specific network that matches this IP address.
        net = IPNetwork(ip)
        while net not in _geo_data:
            net.prefixlen -= 1
        return _geo_data[net]
    except AddrFormatError:
        return ('9000.1', '9000.1')