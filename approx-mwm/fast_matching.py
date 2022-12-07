# https://web.eecs.umich.edu/~pettie/papers/ApproxMWM-JACM.pdf
import math
from objects.matching import Matching

# class Edge:
#     def __init__(self, a, b):
#         self.points = [a, b]
#         self.points.sort()

def edge(a, b):
    pair = [a, b]
    pair.sort()
    return pair

def multiple(a, b):
    return a % b == 0 and a / b > 0

def get_G_elig(vertices, Matching, Omega_edges, weights, delta, yz):
    # At scale i, an edge e is eligible if:
    # e is an edge within a blossom of Omega
    # e is not in M and yz(e) = w_i(e) - delta_i
    # e is in M and yz(e) - w_i(e) is a nonnegative integer multiple of delta_i
    edges = set()
    for first in vertices:
        for second in vertices[first]:
            # Is this edge eligible?
            edge = edge(first, second)
            flag = False
            if edge in Omega_edges:
                flag = True
            elif edge not in Matching and yz[edge] == weights[edge] - delta:
                flag = True
            elif edge in Matching and multiple(yz[edge] - weights[edge], delta):
                flag = True
            if flag:
                edges.add(edge)
    return edges
                

         

def fast_matching(vertices):
    N = len(vertices.keys())
    epsilon = 1/16
    # epsilon_prime = Theta(epsilon)
    epsilon_prime = epsilon

    # Matching = null
    matching = Matching(vertices)
    # Omega = null
    Omega = set()
    Omega_edges = set()
    # delta_0 = epsilon_prime * N
    delta = epsilon_prime * N
    # y(u) = N / 2 - delta_0 / 2, for all u in V(G)
    y_u = N / 2 - delta / 2
    y = dict([(vertex, y_u) for vertex in vertices])
    edges = set()
    for first in vertices:
        for second in vertices[first]:
            # Is this edge eligible?
            edge = edge(first, second)
            edges.add(edge)
    yz = dict([(edge, 0) for edge in edges])
    weights = dict([(edge, 1) for edge in edges])

    # Execute scales i = 0, ..., L = log N and return the matching M

    L = math.ceil(math.log(N))
    for i in range(L + 1):

        # Scale i:

        # Repeat the four steps until:
        # * y-values of free vertices reach N / (2^(i+2)) - delta_i / 2
        # * i in [0, L)
        # * i = L

        # (1) Augmentation:
        # Find a maximal set Psi of vertex-disjoint augmenting paths in G_elig
        Psi = max_augmenting_paths(G_elig)
        # Set M = M (+) (Union P, for all P in Psi)
        # Update G_elig
        G_elig = get_G_elig(vertices=vertices, Matching=Matching, Omega_edges=Omega_edges, weights=weights, delta=delta, yz=yz)

        # (2) Blossom Shrinking:
        # Let V_out be a subset of V(G_elig) be the vertices (that is, root blossoms) reachable from free vertices by even-length alternating paths;
        # Let Omega_prime be a maximal set of (nested) blossoms on V_out.
        # (That is, if (u, v) is in E(G_elig) \ M and u, v is in V_out, then u and v must be in a common blossom.)
        # Let V_in be a subset of V(G_elig) \ V_out, those non-V_out-vertices reachable from free vertices by odd-length alternating paths.
        # Set z(B) = 0 for B in Omega_prime and set Omega = Omega union Omega_prime.
        # Update G_elig


        # (3) Dual Adustment:
        # Let V-hat_in, V-hat_out be subsets of V, the original vertices represented by vertices in V_in and V_out.
        # The y- and z-values for some vertices and root blossoms are adjusted:
        # y(u) = y(u) - delta_i / 2 if u in V-hat_out
        # y(u) = y(u) + delta_i / 2 if u in V-hat_in
        # z(B) = z(B) + delta_i, if B is in Omega and is a root blossom with B is a subset of V-hat_out
        # z(B) = z(B) - delta_i, if B is in Omega and is a root blossom with B is a subset of V-hat_in
        
        # (4) Blossom Dissolution:
        # After dual adjustments some root blossoms may have zero z-values. Dissolve such blossoms (remove them from Omega) as long as they exist. Note that non-root blossoms are allowed to have zero z-values.
        # Update G_elig by the new Omega

        # Prepare for the next scale, if i is in [0, L)
        # delta_(i+1) = delta_i / 2
        # y(u) = y(u) + delta_(i+1) for all u in V(G)
        # (this makes free vertices' y-values become N/2^(i+2))
        pass            



def fast_matching_old(vertices):
    N = len(vertices.keys)
    epsilon = 1/16
    # epsilon_prime = Theta(epsilon)
    epsilon_prime = epsilon

    # Matching = null
    Matching = set()
    # Keep track of free and matched vertices
    Free = set()
    Matched = set()
    # Omega = null
    Omega = set()
    Omega_edges = set()
    # delta_0 = epsilon_prime * N
    delta = epsilon_prime * N
    # y(u) = N / 2 - delta_0 / 2, for all u in V(G)
    y_u = N / 2 - delta / 2
    y = dict([(vertex, y_u) for vertex in vertices])
    edges = set()
    for first in vertices:
        for second in vertices[first]:
            # Is this edge eligible?
            edge = edge(first, second)
            edges.add(edge)
    yz = dict([(edge, 0) for edge in edges])
    weights = dict([(edge, 1) for edge in edges])

    # Execute scales i = 0, ..., L = log N and return the matching M

    L = math.ceil(math.log(N))
    for i in range(L + 1):

        # Scale i:

        # Repeat the four steps until:
        # * y-values of free vertices reach N / (2^(i+2)) - delta_i / 2
        # * i in [0, L)
        # * i = L

        # (1) Augmentation:
        # Find a maximal set Psi of vertex-disjoint augmenting paths in G_elig
        Psi = max_augmenting_paths(G_elig)
        # Set M = M (+) (Union P, for all P in Psi)
        # Update G_elig
        G_elig = get_G_elig(vertices=vertices, Matching=Matching, Omega_edges=Omega_edges, weights=weights, delta=delta, yz=yz)

        # (2) Blossom Shrinking:
        # Let V_out be a subset of V(G_elig) be the vertices (that is, root blossoms) reachable from free vertices by even-length alternating paths;
        # Let Omega_prime be a maximal set of (nested) blossoms on V_out.
        # (That is, if (u, v) is in E(G_elig) \ M and u, v is in V_out, then u and v must be in a common blossom.)
        # Let V_in be a subset of V(G_elig) \ V_out, those non-V_out-vertices reachable from free vertices by odd-length alternating paths.
        # Set z(B) = 0 for B in Omega_prime and set Omega = Omega union Omega_prime.
        # Update G_elig


        # (3) Dual Adustment:
        # Let V-hat_in, V-hat_out be subsets of V, the original vertices represented by vertices in V_in and V_out.
        # The y- and z-values for some vertices and root blossoms are adjusted:
        # y(u) = y(u) - delta_i / 2 if u in V-hat_out
        # y(u) = y(u) + delta_i / 2 if u in V-hat_in
        # z(B) = z(B) + delta_i, if B is in Omega and is a root blossom with B is a subset of V-hat_out
        # z(B) = z(B) - delta_i, if B is in Omega and is a root blossom with B is a subset of V-hat_in
        
        # (4) Blossom Dissolution:
        # After dual adjustments some root blossoms may have zero z-values. Dissolve such blossoms (remove them from Omega) as long as they exist. Note that non-root blossoms are allowed to have zero z-values.
        # Update G_elig by the new Omega

        # Prepare for the next scale, if i is in [0, L)
        # delta_(i+1) = delta_i / 2
        # y(u) = y(u) + delta_(i+1) for all u in V(G)
        # (this makes free vertices' y-values become N/2^(i+2))
        pass