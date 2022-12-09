import sys
import random
random.seed(477)

def id(i, n):
    size = len(hex(n - 1)[2:])
    return hex(i)[2:].zfill(size)

def main(n, m):
    edges = []
    vertices = dict([(i, id(i, n)) for i in range(n)])
    while len(edges) < m:
        # Make an edge
        first = vertices[random.randint(0, n - 1)]
        second = vertices[random.randint(0, n - 1)]
        edge = first + " " + second
        edge1 = second + " " + first
        if first != second and edge not in edges and edge1 not in edges:
            edges.append(edge)
    
    print(f"{n} {m}")
    for edge in edges:
        print(edge)

def main2(n, m):
    vertices = dict([(i, id(i, n)) for i in range(n)])
    possible_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edge = f"{vertices[i]} {vertices[j]}" if random.random() > 0.5 else f"{vertices[j]} {vertices[i]}"
            possible_edges.append(edge)
    edges = random.sample(possible_edges, m)
    print(f"{n} {m}")
    for edge in edges:
        print(edge)

def main3(n, m):
    vertices = dict([(i, id(i, n)) for i in range(n)])
    edges = []
    for x in range(m):
        i = random.randrange(0, n)
        j = random.randrange(0, n)
        edge = f"{vertices[i]} {vertices[j]}" if random.random() > 0.5 else f"{vertices[j]} {vertices[i]}"
        if i != j and edge not in edges:
            edges.append(edge)
    print(f"{n} {len(edges)}")
    for edge in edges:
        print(edge)

if __name__ == "__main__":
    # python3 generate.py 10 30 > graph.out
    if len(sys.argv) != 3:
        print("Parameters: python3 generate.py [n] [m] > [graph.out]")
    else:
        n = int(sys.argv[1])
        m = int(sys.argv[2])
        max_m = int(n * (n - 1) / 2)
        if m > max_m:
            # print(f"Max m is f{max_m}")
            m = max_m
        main3(n, m)