# from matching import Matching
import sys
sys.path.append("..")
from objects.matching import Matching
from objects.edge import Edge, Edge_List
from functions.maximal_set import find_maximal_set
from objects.blossoms import Blossoms

class Graph:
    def __init__(self, vertices, edges, adj_matrix):
        self.vertices = vertices
        self.edges = edges
        self.adj_matrix = adj_matrix

        N = len(vertices)
        epsilon_prime = 1/16
        self.delta = epsilon_prime * N
        y_u = N / 2 - self.delta / 2

        self.yz = dict([(edge, 0) for edge in edges])
        self.y = dict([(vertex, y_u) for vertex in vertices])
        self.w = dict([(edge, 1) for edge in edges])

        self.eligible_e = set()
        self.matching = Matching(vertices)
        self.blossoms = Blossoms()

    def yz(self, u, v):
        # Calculate yz
        return self.y[u] - self.y[v] + self.blossoms.sum_z(u, v)

    def get_g_elig(self):
        self.eligible_e = set()
        for edge in self.edges:
            if (
                (self.blossoms.inBlossom(edge))
                or (
                    (not self.matching.inMatching())
                    and (self.yz[edge] == self.w[edge] - self.delta)
                )
                or (
                    (self.matching.inMatching())
                    and (multiple(self.yz[edge] - self.w[edge], self.delta))
                )
            ):
                # Eligible!
                self.eligible_e.add(edge)

    def step1(self):
        self.get_g_elig()
        # Find a maximal set Psi of vertex-disjoin augmenting paths in G_elig and set M to include this. Update G_elig
        find_maximal_set(self.adj_matrix, self.matching, lambda edge: True)
        # find_maximal_set(self.adj_matrix, self.matching, lambda edge: edge in self.eligible_e)
        # self.matching.add_augmenting_path()
        self.get_g_elig()
    
    def DFS_mark_parity(self, parity, v_out, v_in, v, this_parity, path):
        if v in parity:
            if parity[v] != this_parity:
                # We have already visited this vertex and marked it the other way, meaning this is part of a blossom
                # self.blossoms.add_blossom(v, path)
                print(f"Found a blossom for {v} with a path {path}")
                return
            else:
                # We already visited this, but this doesn't matter
                return
        else:
            # Not yet marked!
            if this_parity == 'out':
                v_out.add(v)
                parity[v] = 'out'

                # mark neighbors!
                for neighbor in self.adj_matrix[v]:
                    if neighbor in self.eligible_e:
                        self.DFS_mark_parity(parity, v_out, v_in, v, 'in', [*path, neighbor])
            else:
                v_in.add(v)
                parity[v] = 'in'

                # mark neighbors!
                for neighbor in self.adj_matrix[v]:
                    if neighbor in self.eligible_e:
                        self.DFS_mark_parity(parity, v_out, v_in, v, 'out', [*path, neighbor])

    def step2(self):
        parity = dict()
        
        # Calculate V_out and V_in
        v_out = set()
        v_in = set()

        self.blossoms.new_blossoms()

        # Starting at free vertices, find what root blossoms are reachable at an even length path
        free_vertices = self.matching.unmatched
        for free in free_vertices:
            # Mark this as an "OUT" (even parity)
            parity[free] = 'out'
            # Look for what's next
            for neighbor in self.adj_matrix[free]:
                if neighbor in self.eligible_e:
                    self.DFS_mark_parity(parity, v_out, v_in, neighbor, 'in', [free, neighbor])

        print(f"step 2: made parity {parity}, vo {v_out}, vi {v_in}")
        print(self.blossoms.blossoms)
        return

        # Update z(B)
        for blossom in self.blossoms.new_blossoms:
            self.blossoms.reset_z(blossom)

        self.get_g_elig()

        return v_out, v_in

    def step3(self, v_in, v_out):

        pass

    def fast_matching(self):
        # Find the fast matching!
        pass

    def iteration(self):
        # One pass of the algorithm
        self.step1()
        v_out, v_in = self.step2()
        self.step3(v_in=v_in, v_out=v_out)
        self.step4()


# Is x a multiple of y, or is x = ny?
def multiple(x, y):
    return x % y == 0


if __name__ == "__main__":
    
    vertices = {
        "A": ["B"],
        "B": ["C","A"],
        "C": ["H","D"],
        "D": ["C", "E"],
        "E": ["D", "F"],
        "F": ["E", "G"],
        "G": ["F", "H"],
        "H": ["G", "C"],
    }

    graph = Graph(vertices.keys(), edges=Edge_List(vertices), adj_matrix=vertices)
    # matching = Matching(vertices)
    # # matching.add("B", "C")
    # # matching.add("D", "E")
    # # matching.add("G", "H")
    # random_matching(vertices, matching)

    print(f"Started with {graph.matching}")
    graph.get_g_elig()
    graph.step2()
    # new_matching = find_maximal_set(vertices, matching)
    print(f"Now have {graph.matching}")