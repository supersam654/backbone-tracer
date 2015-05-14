"""
Convert the GeoLite2 IPv4 database (actually CSV) into an easier format for processing.

Transforms the CSV with lots of information into two files:
ips.txt.gz: newline-separated file of ip addresses ("192.168.1.1\n127.0.0.1"\n...).
geo.txt.gz: Geo data for all of the IP ranges given by GeoLite. Format:

    ipblock[space]latitude[space]longitude
    129.168.1.0/24 1.234 5.6789

As the GeoLite data is licensed under Creative Commons Attribution 3.0 Unported (CC BY-SA 3.0),
the data this outputs is also licensed under CC BY-SA 3.0.
"""

import csv
import gzip
from netaddr import IPNetwork

# Note that the input file is not included with the project. It can be downloded from:
# http://dev.maxmind.com/geoip/geoip2/geolite2/
IN_FILENAME = "data/GeoLite2-City-Blocks-IPv4.csv"
OUT_GEO_FILENAME = "data/geolite.txt.gz"
OUT_IP_FILENAME = "data/ips.txt.gz"

def get_ip_from_range(ip_range):
    ip = IPNetwork(ip_range).ip
    return ip + 1

with open(IN_FILENAME) as geolite_file:
    with gzip.open(OUT_GEO_FILENAME, "w") as output_geo_file:
        with gzip.open(OUT_IP_FILENAME, "w") as output_ip_file:
            reader = csv.DictReader(geolite_file)
            for row in reader:
                network = row['network']
                ip = get_ip_from_range(network)
                latitude = row['latitude']
                longitude = row['longitude']
                output_ip_file.write("%s\n" % ip)
                output_geo_file.write("%s %s %s\n" % (network, latitude, longitude))