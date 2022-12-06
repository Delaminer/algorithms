from matching import matching
from display import display

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

# print(vertices)

matching = matching(vertices=vertices)

print(f"largest matching was size {len(matching)}")
print(matching)

# display(vertices, edges)
display(vertices, edges, matching)