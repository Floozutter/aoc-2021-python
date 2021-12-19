INPUTPATH = "input.txt"
INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
reports = tuple(
    tuple(tuple(map(int, line.split(","))) for line in report.strip().split("\n")[1:])
    for report in raw.split("\n\n")
)

rotations = (
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

Point = tuple[int, int, int]

from collections import Counter
from operator import add, sub
def sync_reports(rep_a: tuple[Point, ...], rep_b: tuple[Point, ...]) -> frozenset[Point] | None:
    syncs = Counter()
    for i, r in enumerate(rotations):
        for a in rep_a:
            for b in rep_b:
                d = tuple(map(sub, a, r(*b)))
                syncs[i, d] += 1
    i, d = max(syncs, key = syncs.get)
    print(i, d, syncs[i, d])
    if syncs[i, d] < 12:
        return None
    else:
        return frozenset(rep_a) | frozenset(tuple(map(add, rotations[i](*b), d)) for b in rep_b)
