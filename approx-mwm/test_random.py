import random
from objects.edge import Edge, Edge_Items
from objects.graph import Graph
from functions.sample import get_input_graph
from generate import id
from basic_matching import slow_matching

import cProfile

# random.seed(1)

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
    return vertices, edges, adj_matrix

def compare():
    vertices, edges, adj_matrix = get_graph(24, 40)
    # vertices, edges, adj_matrix = get_graph(100, 100)
    print(edges)
    # print(vertices)
    # print(edges)
    print(adj_matrix)

    graph = Graph(vertices, edges=edges, adj_matrix=adj_matrix)
    print("Random:")
    print(f" * starting with {graph.matching}")
    graph.random()
    print(f" * ending with {graph.matching}")

    print("Brute Force:")
    slow_matching = slow_matching(vertices=adj_matrix)
    print(f" * basic matching: {len(slow_matching)}")
    print(slow_matching)
    

vertices, edges, adj_matrix = get_graph(10000, 2000000)
print('created the graph')
# vertices, edges, adj_matrix = get_graph(1000, 100000)
# graph = Graph(vertices, edges=edges, adj_matrix=adj_matrix)
# graph.random()
# graph.fast_matching()

# matching = slow_matching(vertices=adj_matrix)
# cProfile.run("graph.fast_matching()")
# print(f" fast matching: {len(graph.matching.pairs)}")


# adj_matrix, edges = get_input_graph()
# vertices = set(adj_matrix.keys())
# print(edges)
graph = Graph(vertices, edges=edges, adj_matrix=adj_matrix)
# graph.random()
# print(f'random matching: {graph2.matching}')
# graph = Graph(vertices, edges=edges, adj_matrix=adj_matrix)
# graph.fast_matching()
# print(f'matching: {graph.matching}')
cProfile.run("graph.fast_matching()")


if __name__ == "__main__":
    # compare()
    # cProfile.run("perf()")
    # perf()
    pass