INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
from collections import defaultdict
system = defaultdict(set)
for line in raw.strip().split("\n"):
    a, b = line.split("-")
    system[a].add(b)
    system[b].add(a)

from functools import cache
@cache
def paths(x: str, visited: frozenset[str], h) -> int:
    h = (*h, x)
    if x == "end":
        #print(h)
        return 1
    total = 0
    for cave in system[x]:
        if cave[0].isupper():
            total += paths(cave, visited, h)
        elif cave[0].islower() and cave not in visited:
            total += paths(cave, frozenset((*visited, cave)), h)
    return total
print(paths("start", frozenset(("start",)), ()))

"""
counts = tuple((key, 0) for key in sorted(system.keys()))
from collections import Counter
from functools import cache
@cache
def paths(x: str, counts, h) -> int:
    h = (*h, x)
    if x == "end":
        print(h)
        return 1
    total = 0
    for cave in system[x]:
        i, n = next(((i, p[1]) for i, p in enumerate(counts) if p[0] == cave))
        if cave == "start":
            continue
        elif cave[0].isupper():
            total += paths(cave, counts, h)
        elif cave[0].islower() and n < 2:
            t = list(counts)
            t[i] = (cave, n + 1)
            #print(t)
            total += paths(cave, tuple(t), h)
    return total
"""

from functools import cache
@cache
def paths(x: str, visited: frozenset[str], h, twiced = False) -> int:
    h = (*h, x)
    if x == "end":
        #print(h)
        return 1
    total = 0
    for cave in system[x]:
        if cave == "start":
            continue
        elif cave[0].isupper():
            total += paths(cave, visited, h, twiced)
        elif cave[0].islower():
            if cave not in visited:
                total += paths(cave, frozenset((*visited, cave)), h, twiced)
            elif not twiced:
                total += paths(cave, frozenset(visited), h, True)
    return total
print(paths("start", frozenset(("start",)), ()))
