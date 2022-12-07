from basic_matching import slow_matching
from display import display
from objects.matching import Matching
from functions.maximal_set import random_matching, find_maximal_set

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
        
        edges.append([a, b])
        vertices[a].append(b)
        vertices[b].append(a)

    return vertices, edges

if __name__ == "__main__":
    vertices, edges = get_input_graph()
    # print(vertices)

    # matching = [
    # ['0f2', '2cf'],
    # ['015', '0cc'],
    # ['331', '239'],
    # ['372', '13e'],
    # ['0a7', '097'],
    # ['37c', '1ec'],

    # ]
    slow_matching = slow_matching(vertices=vertices)
    fast_matching = Matching(vertices)
    random_matching(vertices, fast_matching)

    new_matching = find_maximal_set(vertices, fast_matching)

    print(f"largest matching was size {len(slow_matching)}")
    print(slow_matching)
    print(f"largest fast matching was {new_matching}")

    display(vertices, edges, slow_matching)
    display(vertices, edges, new_matching.pairs)