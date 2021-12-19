INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

from collections import Counter, defaultdict
from dataclasses import dataclass, astuple
from typing import final, NamedTuple, Sequence, Callable

@dataclass(frozen = True)
@final
class Point:
    x: int
    y: int
    z: int
    def __add__(self: "Point", other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self: "Point", other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)
    def l1_distance_to(self: "Point", other: "Point") -> int:
        return sum(map(abs, astuple(self - other)))

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
    (i, d), count = syncs.most_common()[0]
    return None if count < 12 else lambda p: rotations[i](p) + d

def synchronize(reports: Sequence[Sequence[Point]]) -> tuple[frozenset[Point], frozenset[Point]]:
    overlaps: dict[int, list[tuple[int, Callable[[Point], Point]]]] = defaultdict(list)
    for i, j in ((i, j) for i in range(len(reports)) for j in range(len(reports)) if i != j):
        f = syncf(reports[i], reports[j])
        if f is not None:
            overlaps[i].append((j, f))
    visited: set[int] = set()
    def collect(i: int) -> tuple[frozenset[Point], frozenset[Point]]:
        beacons = frozenset(reports[i])
        scanners = frozenset((Point(0, 0, 0),))
        for j, f in overlaps[i]:
            if j not in visited:
                visited.add(j)
                b, s = collect(j)
                beacons |= frozenset(map(f, b))
                scanners |= frozenset(map(f, s))
        return beacons, scanners
    return collect(i)

reports = tuple(
    tuple(
        Point(*map(int, line.split(",")))
        for line in report.strip().split("\n")[1:]
    )
    for report in raw.split("\n\n")
)
beacons, scanners = synchronize(reports)
print(len(beacons))
print(max(a.l1_distance_to(b) for a in scanners for b in scanners))
