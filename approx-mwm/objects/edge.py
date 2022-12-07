def Edge(v1, v2):
    return f"{min(v1,v2)},{max(v1,v2)}"

def Edge_Items(edge):
    return edge.split(",")
