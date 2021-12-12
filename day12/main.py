INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
from collections import defaultdict
system = defaultdict(set)
for a, b in (line.split("-") for line in raw.strip().split("\n")):
    system[a].add(b)
    system[b].add(a)

from functools import cache
@cache
def paths_to_end(cave: str, visited: frozenset[int], allow_one_repeat: bool) -> int:
    if cave == "end":
        return 1
    n = 0
    for adjacent in system[cave]:
        if adjacent == "start":
            continue
        elif adjacent[0].isupper():
            n += paths_to_end(adjacent, visited, allow_one_repeat)
        elif adjacent not in visited:
            n += paths_to_end(adjacent, visited | {adjacent}, allow_one_repeat)
        elif allow_one_repeat:
            n += paths_to_end(adjacent, visited, False)
    return n

print(paths_to_end("start", frozenset(), False))
print(paths_to_end("start", frozenset(), True))
