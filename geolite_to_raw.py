"""
Convert the GeoLite2 IPv4 database (actually CSV) into an easier format for processing.

Transforms the CSV with lots of information into lines consisting of:
ip[space]latitude[space]longitude

The IP is a dotted quad calculated by taking the first valid address from each block.

As the GeoLite data is licensed under Creative Commons Attribution 3.0 Unported (CC BY-SA 3.0),
the data this outputs is also licensed under CC BY-SA 3.0.
"""

import csv
import gzip
from netaddr import IPNetwork

# Note that the input file is not included with the project. It can be downloded from:
# http://dev.maxmind.com/geoip/geoip2/geolite2/
IN_FILENAME = "data/GeoLite2-City-Blocks-IPv4.csv"
OUT_FILENAME = "data/geolite.txt.gz"

def get_ip_from_range(ip_range):
    ip = IPNetwork(ip_range).ip
    return ip + 1

with open(IN_FILENAME) as geolite_file:
    with gzip.open(OUT_FILENAME, "w") as output_file:
        reader = csv.DictReader(geolite_file)
        for row in reader:
            ip = get_ip_from_range(row['network'])
            latitude = row['latitude']
            longitude = row['longitude']
            output_file.write("%s %s %s\n" % (ip, latitude, longitude))