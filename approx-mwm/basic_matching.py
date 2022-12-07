from objects.edge import Edge

# Find the matches recursively
def slow_matching(vertices):
    return recurse(vertices, [])
sol = {}
def getkey(ignore):
    return ignore.sort()

def recurse(vertices, ignore):
    key = getkey(ignore)

    if key in sol:
        return sol[key]
    
    best_matching = []
    i = 0
    # if len(ignore) % 10 == 0 and len(ignore) != 50:
    #     print(f"{len(ignore)} - {i}")
    for first in available(vertices, ignore):
        if len(ignore) == 0:
            print(i)
        i += 1
        # Should we match this with someone?
        for second in available(vertices[first], ignore):
            this = recurse(vertices=vertices, ignore=[first, second, *ignore])
            if len(this) >= len(best_matching):
                # Better match!
                best_matching = this.copy()
                best_matching.append(Edge(first, second))
    
    sol[key] = best_matching
    return best_matching

def available(possible, remove):
    for element in possible:
        if element not in remove:
            yield element
