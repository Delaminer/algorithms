# Find the matches recursively
def matching(vertices):
    return recurse(vertices, [])

def recurse(vertices, ignore):
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
                best_matching = this
                best_matching.append([first, second])
    
    return best_matching

def available(possible, remove):
    for element in possible:
        if element not in remove:
            yield element
