from objects.edge import Edge, Edge_Items

class Matching:
    def __init__(self, vertices):
        self.vertices = vertices
        self.clear()
    
    # Clear the matching
    def clear(self):
        self.pairs = []
        self.matched = set()
        self.unmatched = set(self.vertices)
        self.partner = dict([(i, None) for i in self.vertices]) # All vertices have a partner of None
    
    def random(self, adj_matrix):
        # Create a random matching
        for v in self.vertices:
            # Try to match this up
            if not self.isMatched(v):
                for next_v in adj_matrix[v]:
                    if not self.isMatched(next_v):
                        # Match them!
                        self.add(v, next_v)
                        break
        
        print(f'Random matching matched {len(self.matched)}, did not match {len(self.unmatched)}')

    def add(self, v1, v2):
        if v1 in self.matched:
            print(f"{v1} is already matched! (with {self.partner[v1]})")
        if v2 in self.matched:
            print(f"{v2} is already matched! (with {self.partner[v2]})")

        self.matched.add(v1)
        self.matched.add(v2)
        self.partner[v1] = v2
        self.partner[v2] = v1
        self.unmatched.remove(v1)
        self.unmatched.remove(v2)
        new_edge = Edge(v1, v2)
        self.pairs.append(new_edge)
        return new_edge
    
    def remove(self, v):
        if v in self.unmatched:
            print(f"{v} was unmatched")
        
        v2 = self.partner[v]
        
        self.matched.remove(v)
        self.matched.remove(v2)
        self.partner[v] = None
        self.partner[v2] = None
        self.unmatched.add(v)
        self.unmatched.add(v2)
        old_edge = Edge(v, v2)
        self.pairs.remove(old_edge)
        return old_edge
    
    def add_augmenting_path(self, add, remove):
        # print(f'Using Augmenting Path: add {add}, remove {remove}')
        for remove_edge in remove:
            e1, e2 = Edge_Items(remove_edge)
            self.remove(e1)
        for add_edge in add:
            e1, e2 = Edge_Items(add_edge)
            self.add(e1, e2)

    def isMatched(self, v):
        return v in self.matched
    
    def inMatching(self, edge):
        return edge in self.pairs

    def getPartner(self, v):
        return self.partner[v]

    def get_unmatched(self):
        return self.unmatched
    
    def getPair(self, v):
        return [v, self.partner[v]]
    
    def size(self):
        return len(self.pairs)

    def __str__(self):
        self.verbose = False
        return f"Matching({len(self.pairs)} pairs)" + (f": {self.pairs}" if self.verbose else "")