import random
import sys
sys.path.append("..")
from generate import id
from objects.edge import Edge, Edge_Items

random.seed(1)

def get_graph(n, m):
    vertices =  set([id(i, n) for i in range(n)])
    adj_matrix = dict([(i, []) for i in vertices])
    possible_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edge = Edge(id(i, n), id(j, n))
            possible_edges.append(edge)
    edges = random.sample(possible_edges, m)
    for edge in edges:
        first, second = Edge_Items(edge)
        adj_matrix[first].append(second)
        adj_matrix[second].append(first)
    print('Done!')
    return vertices, edges, adj_matrix


def get_input_graph():
    line = input()
    n, m = line.split()
    n = int(n)
    m = int(m)

    vertices = {}
    edges = []

    for i in range(m):
        edge = input()
        a, b = edge.split()
        
        if a not in vertices:
            vertices[a] = []
        if b not in vertices:
            vertices[b] = []
        
        edges.append(Edge(a, b))
        vertices[a].append(b)
        vertices[b].append(a)

    return vertices, edges