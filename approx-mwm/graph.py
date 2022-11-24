from matching import matching
from display import display

line = input()
num_edges, max_letter = line.split()
num_edges = int(num_edges)
num_vertices = 1 + ord(max_letter) - ord('A')

vertices = {}

for i in range(num_edges):
    edge = input()
    a, b = edge.split()
    
    if a not in vertices:
        vertices[a] = []
    if b not in vertices:
        vertices[b] = []
    
    vertices[a].append(b)
    vertices[b].append(a)

print(vertices)

matching = matching(vertices=vertices)

print(f"largest matching was size {len(matching)}: {matching}")

display(vertices, matching)