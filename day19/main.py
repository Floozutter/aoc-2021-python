INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

from itertools import chain
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import NamedTuple, Sequence, Callable

@dataclass(frozen = True)
class Point:
    x: int
    y: int
    z: int
    def __add__(self: "Point", other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self: "Point", other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

rotations: Sequence[Callable[[Point], Point]] = (
    lambda p: Point(+p.x, +p.y, +p.z),
    lambda p: Point(+p.x, -p.y, -p.z),
    lambda p: Point(+p.x, +p.z, -p.y),
    lambda p: Point(+p.x, -p.z, +p.y),
    lambda p: Point(-p.x, +p.y, -p.z),
    lambda p: Point(-p.x, -p.y, +p.z),
    lambda p: Point(-p.x, +p.z, +p.y),
    lambda p: Point(-p.x, -p.z, -p.y),
    lambda p: Point(+p.y, +p.z, +p.x),
    lambda p: Point(+p.y, -p.z, -p.x),
    lambda p: Point(+p.y, +p.x, -p.z),
    lambda p: Point(+p.y, -p.x, +p.z),
    lambda p: Point(-p.y, +p.z, -p.x),
    lambda p: Point(-p.y, -p.z, +p.x),
    lambda p: Point(-p.y, +p.x, +p.z),
    lambda p: Point(-p.y, -p.x, -p.z),
    lambda p: Point(+p.z, +p.x, +p.y),
    lambda p: Point(+p.z, -p.x, -p.y),
    lambda p: Point(+p.z, +p.y, -p.x),
    lambda p: Point(+p.z, -p.y, +p.x),
    lambda p: Point(-p.z, +p.x, -p.y),
    lambda p: Point(-p.z, -p.x, +p.y),
    lambda p: Point(-p.z, +p.y, +p.x),
    lambda p: Point(-p.z, -p.y, -p.x),
)

def syncf(rep_a: Sequence[Point], rep_b: Sequence[Point]) -> Callable[[Point], Point] | None:
    syncs: Counter[tuple[int, Point]] = Counter()
    for i, r in enumerate(rotations):
        for a in rep_a:
            for b in rep_b:
                syncs[i, a - r(b)] += 1
    (i, d), count = max(syncs.items(), key = lambda pair: pair[1])
    return None if count < 12 else lambda p: rotations[i](p) + d

def synchronize(reports: Sequence[Sequence[Point]]) -> frozenset[Point]:
    overlaps: dict[int, list[tuple[int, Callable[[Point], Point]]]] = defaultdict(list)
    for i, j in ((i, j) for i in range(len(reports)) for j in range(len(reports)) if i != j):
        f = syncf(reports[i], reports[j])
        if f is not None:
            overlaps[i].append((j, f))
    visited: set[int] = set()
    def collect(i: int) -> frozenset[Point]:
        visited.add(i)
        return frozenset(reports[i]) | frozenset(chain.from_iterable(
            map(f, collect(j))
            for j, f in overlaps[i]
            if j not in visited
        ))
    return collect(0)

reports: Sequence[Sequence[Point]] = tuple(
    tuple(
        Point(*map(int, line.split(",")))
        for line in report.strip().split("\n")[1:]
    )
    for report in raw.split("\n\n")
)
print(len(synchronize(reports)))
