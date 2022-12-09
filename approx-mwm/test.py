import cProfile
import test_random
cProfile.run("[(a, b) for a in (1, 3, 5) for b in (2, 4, 6)]")