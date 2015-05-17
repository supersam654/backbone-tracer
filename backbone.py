"""
This script is responsible for loading the entire graph of known nodes and
loading up the geolocation database, distilling that down to a very small
subset, and saving it for fast loading.

For example:
    Geo Location database: ~675MB of RAM and ~1min load time.
    All traceroute data: ~1GB uncompressed json (~80MB compressed binary)
    Load time for traceroute data + geo + pruning = ~15min

    Outputs a ~2MB json file that loads in a few seconds and includes all data
    for the most important ~200 nodes.
"""
from itertools import tee, izip
import json
import networkx as nx
from networkx.readwrite import json_graph
import gzip
import struct
from netaddr import IPAddress
import sys

# Keep pruning until there are fewer nodes than N.
N = 200

source = None

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def add_hops_to_graph(G, trace):
    iterable = [[-1, trace['source'], 0]] + trace['hops']
    for hop1, hop2 in pairwise(iterable):
        count1, ip1, time1 = hop1
        count2, ip2, time2 = hop2
        if G.has_edge(ip1, ip2):
            G.edge[ip1][ip2]['weight'] += 1
        else:
            G.add_edge(ip1, ip2, weight=1)

def prune(G, min_weight, source):
    for vertex in G.nodes():
        if sum(G.get_edge_data(*edge)['weight'] for edge in G.edges(vertex)) < min_weight:
            G.remove_node(vertex)
    tree = nx.dfs_tree(G, source)
    connected_vertices = {node for node in tree.nodes()}
    # Remove any orphaned vertexes.
    for vertex in G.nodes():
        if vertex not in connected_vertices:
            G.remove_node(vertex)
    return G

def print_stats(G):
    print "Nodes: %d Edges: %d" % (G.number_of_nodes(), G.number_of_edges())

def calc_format_string(size):
    s = "<QQ" + "QII" * size
    return s

def get_trace(f):
    size = f.read(4)
    if not size: return None
    size = struct.unpack("<I", size)[0]
    format_string = calc_format_string(size)
    format_size = struct.calcsize(format_string)
    data = f.read(format_size)
    trace_data = struct.unpack(format_string, data)
    trace = {}
    trace['source'] = trace_data[0]
    trace['destination'] = trace_data[1]
    trace['hops'] = []
    for i in range(size):
        ip = trace_data[2 + i * 3]
        count = trace_data[3 + i * 3]
        time = trace_data[4 + i * 3]
        
        ip = str(IPAddress(ip))
        trace['hops'].append([count, ip, time])
    return trace

def getGraph():
    count = 0
    sys.stdout.write("Reading data from file and adding to graph")
    sys.stdout.flush()
    G = nx.Graph()
    with gzip.open("data/trace.bin.gz", "rb") as f:
        while True:
            if count % 1e5 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()
            count += 1
            trace = get_trace(f)
            if not trace: break
            last_trace = trace
            add_hops_to_graph(G, trace)
    
    print "\nSetting source"
    global source
    source = last_trace['source']
    print_stats(G)
    return G

G = getGraph()

print "Pruning"
min_weight = 5000 # If you want to prune to a very high number (basically no pruning), set this to 1 instead.
while G.number_of_nodes() > N:
    min_weight += 1
    prune(G, min_weight, source)

print "Pruned the graph!"
print_stats(G)

import geodb
geo_data = {n: geodb.get_geo(n) for n in G.nodes()}

data = {'graph': json_graph.adjacency_data(G), 'geo': geo_data}
with open("data/backbone.json", "w") as f:
    json.dump(data, f)
