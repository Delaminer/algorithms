def Edge(v1, v2):
    return f"{min(v1,v2)},{max(v1,v2)}"

def Edge_Items(edge):
    return edge.split(",")

def Edge_List(adj_matrix):
    edges = set()
    for first in adj_matrix:
        for second in adj_matrix[first]:
            # Is this edge eligible?
            edge = Edge(first, second)
            edges.add(edge)
    return edge