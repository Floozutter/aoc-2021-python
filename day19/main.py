INPUTPATH = "input.txt"
INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
reports = tuple(
    tuple(tuple(map(int, line.split(","))) for line in report.strip().split("\n")[1:])
    for report in raw.split("\n\n")
)

reorientations = (
    lambda x, y, z: (+x, +y, +z),
    lambda x, y, z: (+x, -y, -z),
    lambda x, y, z: (+x, +z, -y),
    lambda x, y, z: (+x, -z, +y),
    lambda x, y, z: (-x, +y, -z),
    lambda x, y, z: (-x, -y, +z),
    lambda x, y, z: (-x, +z, +y),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (+y, +z, +x),
    lambda x, y, z: (+y, -z, -x),
    lambda x, y, z: (+y, +x, -z),
    lambda x, y, z: (+y, -x, +z),
    lambda x, y, z: (-y, +z, -x),
    lambda x, y, z: (-y, -z, +x),
    lambda x, y, z: (-y, +x, +z),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (+z, +x, +y),
    lambda x, y, z: (+z, -x, -y),
    lambda x, y, z: (+z, +y, -x),
    lambda x, y, z: (+z, -y, +x),
    lambda x, y, z: (-z, +x, -y),
    lambda x, y, z: (-z, -x, +y),
    lambda x, y, z: (-z, +y, +x),
    lambda x, y, z: (-z, -y, -x),
)

def diff(a, b):
    x, y, z = a
    i, j, k = b
    return x - i, y - j, z - k

from itertools import combinations, permutations
from collections import defaultdict
def f(a, b):
    transformations = defaultdict(set)
    for i, r in enumerate(reorientations):
        for a1, a2 in combinations(a, 2):
            for bs in combinations(b, 2):
                for b1, b2 in permutations(bs):
                    d1 = diff(a1, r(*b1))
                    d2 = diff(a2, r(*b2))
                    if d1 == d2:
                        transformations[i, d1].add((a1, b1))
                        transformations[i, d2].add((a2, b2))
    s = max(transformations.values(), key = len)
    print(len(s))
    for a, b in s:
        print(a, b)

f(reports[0], reports[1])
