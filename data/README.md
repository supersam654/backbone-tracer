# What is this?

This product includes GeoLite data created by MaxMind, available from 
<a href="http://www.maxmind.com">http://www.maxmind.com</a>.

The file `geolite.txt.gz` is directly created by extracting any relevant (for
this project) information, compressing it, and saving it. This process can be
replicated by running:

    python geolite_to_raw.py

The file `data.json.gz` is created by running traceroutes on the the data
from `geolite.txt.gz`. Therefore, both `data.json.gz` and `geolite.txt.gz` are
both licensed under CC BY-SA 3.0, just as the original GeoLite2 data is.