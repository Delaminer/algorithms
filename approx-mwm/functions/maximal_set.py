import sys
sys.path.append("..")
from objects.matching import Matching
from objects.edge import Edge

def DFS(vertices, matching, visited, v, ff):
    if v in visited:
        return 0, set(), set()
    else:
        visited.add(v)

        best_score, best_add, best_remove = 0, set(), set()

        # Find just a normal unmatched vertex we can connect to
        for next_v in vertices[v]:
            if not matching.isMatched(next_v):
                best_score = 1
                best_add.add(Edge(v, next_v))

        # Find another (matched) vertex we can connect to
        for next_v in vertices[v]:
            if matching.isMatched(next_v):
                # Found a matched vertex. Remove its match and match with it. That other vertex is now unmatched, so DFS on it.

                # Get the other edge
                next_next_v = matching.getPartner(next_v)
                # Remove the match
                toRemove = matching.remove(next_v)
                # Add this new match
                toAdd = matching.add(v, next_v)

                # Next, match up next_next_v!
                this_score, this_add, this_remove = DFS(vertices, matching, visited, next_next_v, ff + "  ")

                # Undo this matching
                matching.remove(v)
                matching.add(next_v, next_next_v)

                if this_score > best_score:
                    best_score = this_score
                    # Use this augmenting path
                    best_add = this_add
                    best_remove = this_remove
                    # add the edge we add and remove
                    best_add.add(toAdd)
                    best_remove.add(toRemove)

        visited.remove(v)

        return best_score, best_add, best_remove

def find_maximal_set(vertices, matching):
    visited = set() # Set
    unmatched = matching.get_unmatched()

    while len(unmatched) > 0:
        flag = True
        for v in unmatched:
            this_score, this_add, this_remove = DFS(vertices, matching, visited, v, "")
            if this_score != 0:
                matching.add_augmenting_path(this_add, this_remove)
                flag = False
                break
            # unmatched = matching.get_unmatched()
        # No modifications!
        if flag:
            break
        unmatched = matching.get_unmatched()

        # if this_score > best_score:
        #     # Use this augmenting path
        #     best_add = this_add
        #     best_remove = this_remove
    
    # Use the best augmenting path

    
    # while len(toSearch) > 0:
    #     v = toSearch.pop()
    #     # Can we start with this unmatched vertex?
    #     for v_next in vertices[v]:
    #         if not matched[v_next]:
    #             # Is this matched?
    #             include.append(v)
    #             include.append(v_next)
    return matching

def random_matching(vertices, matching):
    for v in vertices.keys():
        # Try to match this up
        if matching.isMatched(v):
            continue
        else:
            for next_v in vertices[v]:
                if not matching.isMatched(next_v):
                    # Match them!
                    matching.add(v, next_v)
                    break


def test_maximal_set():
    # vertices, edges = get_input_graph()
    # vertices = {
    #     "A": ["B"],
    #     "B": ["C","A"],
    #     "C": ["B","D"],
    #     "D": ["C", "E"],
    #     "E": ["D", "F"],
    #     "F": ["E"],
    # }
    # matching = Matching(vertices)
    # matching.add("B", "C")
    # matching.add("D", "E")
    
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
    matching = Matching(vertices)
    # matching.add("B", "C")
    # matching.add("D", "E")
    # matching.add("G", "H")
    random_matching(vertices, matching)

    print(f"Started with {matching}")
    new_matching = find_maximal_set(vertices, matching)
    print(f"Now have {new_matching}")
    print(f"(also have {matching})")

if __name__ == "__main__":
    test_maximal_set()