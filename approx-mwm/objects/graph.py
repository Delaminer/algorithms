import sys
import math
import random

sys.path.append("..")

from display import display

from objects.matching import Matching
from objects.edge import Edge, Edge_List, Edge_Items
from objects.blossoms import Blossoms

from functions.maximal_set import find_maximal_set
from functions.sample import get_graph, get_input_graph


class Graph:
    def __init__(self, vertices, edges, adj_matrix, weights=None):
        self.vertices = set(vertices)
        self.edges = edges
        self.adj_matrix = adj_matrix

        self.N = len(vertices)
        epsilon_prime = 1 / 16
        self.delta = epsilon_prime * self.N
        y_u = self.N / 2 - self.delta / 2

        # self.yz = dict([(edge, 0) for edge in edges])
        self.y = dict([(vertex, y_u) for vertex in vertices])
        # self.w = dict([(edge, random.randint(1, 10)) for edge in edges])
        self.w = weights if weights is not None else dict([(edge, random.randint(1, 10)) for edge in edges])

        self.eligible_e = set()
        self.eligible_v = set()
        self.matching = Matching(vertices)
        self.blossoms = Blossoms(vertices)

    def display(self):
        display(
            self.adj_matrix,
            [Edge_Items(edge) for edge in self.edges],
            self.matching.pairs,
        )

    def random(self):
        self.matching.random(self.adj_matrix)

    def use_matching(self, matches):
        self.matching.clear()
        for match in matches:
            self.matching.add(match[0], match[1])

    def yz(self, edge):
        # Calculate yz
        u, v = Edge_Items(edge)
        return self.y[u] - self.y[v] + self.blossoms.sum_z(u, v)

    def update_g_elig(self):
        self.eligible_e = set()
        self.eligible_v = set()
        for edge in self.edges:
            if (self.blossoms.inBlossom(edge)) or (
                (self.yz(edge) - self.w[edge] % self.delta == 0)
                if (self.matching.inMatching(edge))
                else (self.yz(edge) == self.w[edge] - self.delta)
            ):
                # Eligible!
                self.eligible_e.add(edge)
                first, second = Edge_Items(edge)
                self.eligible_v.add(first)
                self.eligible_v.add(second)
                # print(f"{edge} is eligible")
            # else:
            #     print(f"{edge} is not eligible")
        # self.eligible_e = self.edges.copy()
        # print(self.vertices)
        # self.eligible_v = self.vertices.copy()

    def DFS_mark_parity(self, parity, v_out, v_in, v, this_parity, path, prev=None):
        print(f"Adding path {path}")
        if v in parity:
            if parity[v] != this_parity and path.index(v) < len(path) - 1:
                # We have already visited this vertex and marked it the other way, meaning this is part of a blossom
                # self.blossoms.add_blossom(v, path)

                # Determine which vertices are part of the blossom:
                parity[v] = "out"
                blossom_members = path[path.index(v) : -1]
                # print(f"Found a blossom for {v} with a path {path} -> {blossom_members}")

                self.blossoms.add_blossom(blossom_members)

                for other_v in blossom_members:
                    if parity[other_v] == "in":
                        v_in.remove(other_v)
                        v_out.add(other_v)
                        parity[other_v] = "out"
                return
            else:
                # We already visited this, but this doesn't matter
                return
        else:
            # Not yet marked!
            if this_parity == "out":
                v_out.add(v)
                parity[v] = "out"

                # mark neighbors!
                for neighbor in self.adj_matrix[v]:
                    if neighbor in self.eligible_v and neighbor != prev:
                        self.DFS_mark_parity(
                            parity,
                            v_out,
                            v_in,
                            neighbor,
                            "in",
                            [*path, neighbor],
                            prev=v,
                        )
            else:
                v_in.add(v)
                parity[v] = "in"

                # mark neighbors!
                for neighbor in self.adj_matrix[v]:
                    if neighbor in self.eligible_v and neighbor != prev:
                        self.DFS_mark_parity(
                            parity,
                            v_out,
                            v_in,
                            neighbor,
                            "out",
                            [*path, neighbor],
                            prev=v,
                        )

    # Augmentation
    def step1(self):
        # Find a maximal set Psi of vertex-disjoin augmenting paths in G_elig and set M to include this. Update G_elig
        # find_maximal_set(self.adj_matrix, self.matching, lambda edge: True)
        find_maximal_set(
            self.adj_matrix, self.matching, lambda edge: edge in self.eligible_e
        )
        # self.matching.add_augmenting_path()
        self.update_g_elig()

    # Blossom Shrinking
    def step2(self):
        parity = dict()
        v_out = set()
        v_in = set()

        # Starting at free vertices, find what root blossoms are reachable at an even length path
        # Mark those as "out" and be a part of v_out.
        free_vertices = self.matching.unmatched
        for free in free_vertices:
            # Mark this as an "OUT" (even parity)
            parity[free] = "out"
            v_out.add(free)
            # Look for what's next
            for neighbor in self.adj_matrix[free]:
                if neighbor in self.eligible_v:
                    # print('visiting ')
                    self.DFS_mark_parity(
                        parity, v_out, v_in, neighbor, "in", [free, neighbor], prev=free
                    )

        # print(f"step 2: made parity {parity}, vo {v_out}, vi {v_in}")
        # print(self.blossoms.union_find.parent)
        # print(self.blossoms.union_find.size)
        # return

        # # Update z(B)
        # for blossom in self.blossoms.new_blossoms:
        #     self.blossoms.reset_z(blossom)

        self.update_g_elig()

        return v_out, v_in

    # Dual Adjustment
    def step3(self, v_in, v_out):
        for v in v_out:
            self.y[v] -= self.delta / 2
        for v in v_in:
            self.y[v] += self.delta / 2
        for b in self.blossoms.union_find.unique:
            if b in v_out:
                # All of the blossom must be in v_out
                if b not in self.blossoms.z:
                    self.blossoms.z[b] = 0
                self.blossoms.z[b] += self.delta
            elif b in v_in:
                if b not in self.blossoms.z:
                    self.blossoms.z[b] = 0
                self.blossoms.z[b] -= self.delta

    # Blossom Dissolution
    def step4(self):
        self.blossoms.dissolve()
        self.update_g_elig()

    def iteration(self):
        # One pass of the algorithm
        self.update_g_elig()
        self.step1()
        v_out, v_in = self.step2()
        self.step3(v_in=v_in, v_out=v_out)
        self.step4()

    def fast_matching(self):
        L = math.ceil(math.log(self.N))
        for i in range(L + 1):
            print(f'Scale {i}')
            target = (self.N / (2 ** (i + 2))) - (self.delta / 2)
            while True:
                self.iteration()
                flag = True
                for v in self.vertices:
                    if not self.matching.isMatched(v):
                        # Free vertex, check if it has reached its target (depending on i)
                        if self.y[v] <= (0 if (i == L) else target):
                            # It has not, we need to loop another time
                            flag = False
                            break
                if flag:
                    break
            
            # For the next scale:
            self.delta /= 2
            for v in self.vertices:
                self.y[v] += self.delta

def test1():
    vertices, edges, adj_matrix = get_graph(20, 40)

    graph = Graph(vertices, edges=edges, adj_matrix=adj_matrix)
    graph.random()

    print(f"Started with {graph.matching}")
    graph.update_g_elig()
    graph.step2()
    # new_matching = find_maximal_set(vertices, matching)
    print(f"Now have {graph.matching}")


def test2():
    vertices = {
        "A": ["B"],
        "B": ["C", "A"],
        "C": ["H", "D"],
        "D": ["C", "E"],
        "E": ["D", "F"],
        "F": ["E", "G"],
        "G": ["F", "H"],
        "H": ["G", "C"],
    }

    # vertices, edges, adj_matrix = get_graph(20, 40)

    adj_matrix = {
        "a": ["b"],
        "b": ["a", "c"],
        "c": ["b"],
        "d": ["e"],
        "e": ["d", "f"],
        "f": ["e"],
        "1": ["2"],
        "2": ["1", "3"],
        "3": ["2", "4", "7"],
        "4": ["3", "5"],
        "5": ["4", "6"],
        "6": ["5", "7"],
        "7": ["6", "3"],
    }
    vertices = set(adj_matrix.keys())
    print(vertices)
    edges = Edge_List(adj_matrix)

    initial_matching = [
        ["b", "c"],
        ["e", "f"],
        ["2", "3"],
        ["4", "5"],
        ["6", "7"],
    ]

    # print(edge_list)
    vertices, edges, adj_matrix = get_graph(1000, 5000)
    weights = dict([(edge, random.randint(1, 100)) for edge in edges])
    graph_random = Graph(vertices, edges=edges, adj_matrix=adj_matrix, weights=weights)
    graph_random.random()
    score_random = 0
    for edge in graph_random.matching.pairs:
        score_random  += weights[edge]
    print(f'Random matching: {graph_random.matching}, score = {score_random}')

    graph = Graph(vertices, edges=edges, adj_matrix=adj_matrix, weights=weights)

    # Set matching to this specific state
    # graph.use_matching(initial_matching)

    # graph.display()
    # graph.step2()

    graph.fast_matching()
    score = 0
    for edge in graph.matching.pairs:
        score  += weights[edge]
    print(f'Approx matching: {graph.matching}, score = {score}')


def test3():
    adj_matrix, edges = get_input_graph()
    vertices = set(adj_matrix.keys())
    # print(edges)
    graph2 = Graph(vertices, edges=edges, adj_matrix=adj_matrix)
    graph2.random()
    print(f'random matching: {graph2.matching}')
    graph = Graph(vertices, edges=edges, adj_matrix=adj_matrix)
    graph.fast_matching()
    print(f'matching: {graph.matching}')


if __name__ == "__main__":
    test3()
