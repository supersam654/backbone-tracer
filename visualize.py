from itertools import tee, izip
import json
import gzip
import networkx as nx
import mpld3

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

def print_stats(G):
    print "Nodes: %d Edges: %d" % (len(G.nodes()), len(G.edges()))

def getGraph():
    print "Reading data from file..."
    data = []
    with gzip.open("save.json.gz") as f:
        for line in f:
            data.append(json.loads(line))
    
    print "Adding data to graph..."
    G = nx.Graph()
    global source
    source = data[0]['source']
    for trace in data:
        add_hops_to_graph(G, trace)
    print_stats(G)
    return G

G = getGraph()
backbone = prune(G.copy(), 4000, source)

#print "Drawing..."
#nx.draw(G)
#print "Showing.."
#mpld3.show()