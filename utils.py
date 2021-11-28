import numpy as np

MINDIST=1e-5

class Status:
    FREE = 0
    OCCUPIED = 1
    START = 2
    END = 3
    VISITED=4

def find_pairs(nodelist):
    n = len(nodelist)
    return [(nodelist[i], nodelist[j]) for i in range(n) for j in range(i+1, n)]

def nodalDistance(node1, node2):
    loc1 = node1.loc
    loc2 = node2.loc
    return np.linalg.norm(loc2-loc1)

def form_graph(edges):
    shortest_edges = []
    # min_d = np.Inf
    for node_1, node_2 in edges:
        d = nodalDistance(node_1, node_2)
        if d <= 2:
            # min_d = d
            shortest_edges.append((node_1, node_2))   
    return shortest_edges

def location(points, point):
    return np.where(np.all(points==point, axis=1))[0]