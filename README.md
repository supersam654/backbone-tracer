# Backbone Tracer

This project aims to traceroute the internet!

## Requirements

Have a working scientific Python (2.7 :( - sorry) environment setup. Specifically, you will need:

* Python 2.7
* networkx (visualization only)
* ipgetter (tracing only)
* mpld3 (visualization only)

## Tracing and Visualizing

This project is built on two rather distinct parts. The first part is based on tracerouting the internet! The second part is all about visualizing everything.

## Tracing

To traceroute the internet, run:

    python traceroute.py <filename>

By default, filename should be `data/geolite.txt.gz`