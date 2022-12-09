from objects.edge import Edge_Items
class Blossoms:
    def __init__(self, vertices):
        self.z = dict()
        self.vertices = vertices
        self.union_find = UnionFind(vertices)

    def inBlossom(self, edge):
        first, second = Edge_Items(edge)
        # This edge is in a blossom if both ends are in the same blossom
        return self.union_find.find(first) == self.union_find.find(second)
    
    def add_blossom(self, blossom_members):
        print(f"Calling add_blossom with input {blossom_members}")
        first = blossom_members[0]
        for bm in blossom_members:
            if bm != first:
                self.union_find.union(first, bm)
        this_blossom = self.union_find.find(first)
        self.z[this_blossom] = 0

    def reset_z(self, blossom):
        return self.z[blossom]

    # Return the z values of every blossom that contains this edge
    def sum_z(self, u, v):
        u_blossom = self.union_find.find(u)
        v_blossom = self.union_find.find(v)
        
        return (u_blossom in self.z) and (v_blossom in self.z) and (self.z[u_blossom] + self.z[u_blossom] if u_blossom != v_blossom else self.z[u_blossom])

    def dissolve(self):
        # Dissolve all root blossoms that have zero z-values
        for b in self.union_find.unique:
            if b in self.z and self.z[b] == 0:
                # Dissolve it, making each member become its own blossom
                for v in self.vertices:
                    if self.parent[v] == b:
                        # Disconnect
                        self.union_find.parent[v] = v
                        self.union_find.size[v] = 1
                        self.union_find.unique.add(v)

class UnionFind():
    def __init__(self, vertices):
        self.parent = dict([(v, v) for v in vertices])
        self.size = dict([(v, 1) for v in vertices])
        self.unique = vertices.copy()
    
    def find(self, v):
        if v == self.parent[v]:
            return v
        self.parent[v] = self.find(self.parent[v])
        return self.parent[v]
        
    # Return new_set, old_set
    def union(self, u, v):
        # Which becomes the base?
        # Choose the larger one by size
        root_u = self.find(u)
        root_v = self.find(v)
        total_size = self.size[root_u] + self.size[root_v]

        if self.size[root_u] > self.size[root_v]:
            self.unique.remove(root_v)
            self.size[root_u] = total_size
            self.size[root_v] = total_size
            self.parent[root_v] = root_u
            return root_u, root_v
        else:
            self.unique.remove(root_u)
            self.size[root_u] = total_size
            self.size[root_v] = total_size
            self.parent[root_u] = root_v
            return root_v, root_u
        