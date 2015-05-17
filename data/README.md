# What is this?

This product includes GeoLite data created by MaxMind, available from
[http://www.maxmind.com](http://www.maxmind.com).

The files `geo.txt.gz` and `ips.txt.gz` are directly created by extracting any
relevant (for this project) information, compressing it, and saving it. This
process can be replicated by running:

    python geolite_to_raw.py

The file `data.bin.gz` is created by running traceroutes on the the data
from `ips.txt.gz`. Therefore, both `data.bin.gz` and `geo.txt.gz` are both
licensed under CC BY-SA 3.0, just as the original GeoLite2 data is.

The file `backbone.json.gz` is also created by working with `trace.bin.gz` and
`geo.txt.gz`. Therefore, it is also licensed under CC BY-SA 3.0.