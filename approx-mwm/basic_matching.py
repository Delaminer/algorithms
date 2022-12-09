from objects.edge import Edge

# Find the matches recursively
def slow_matching(vertices, verbose=False):
    ans = recurse(vertices, [], matching=[], verbose=verbose)
    return ans

DP = dict()

def recurse(vertices, ignore, matching, verbose=False):
    key = frozenset(ignore)

    if key in DP:
        return DP[key]
    
    best_matching = []
    i = 0
    for first in vertices:
        if first not in ignore:
            if verbose and len(ignore) == 0:
                print(i)
            i += 1
            # Should we match this with someone?
            for second in vertices[first]:
                if second not in ignore:
                    edge = Edge(first, second)
                    this = recurse(vertices=vertices, ignore=[first, second, *ignore], matching=[*matching, edge], verbose=verbose)
                    if len(this) >= len(best_matching):
                        # Better match!
                        # print(f'new best of {len(this)} using {first}')
                        best_matching = this.copy()
                        best_matching.append(edge)
    
    DP[key] = best_matching
    return best_matching

def available(possible, remove):
    for element in possible:
        if element not in remove:
            yield element
