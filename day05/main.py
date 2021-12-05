INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

Point = tuple[int, ...]
from typing import NamedTuple, Iterator
class Line(NamedTuple):
    start: Point
    end: Point
    def points(self) -> Iterator[Point]:
        diffs = tuple(b - a for a, b in zip(self.start, self.end))
        steps = max(map(abs, diffs))
        strides = tuple(d // steps for d in diffs)
        return (
            Point(s*i + z for z, s in zip(self.start, strides))
            for i in range(steps + 1)
        )
    def axis_aligned(self) -> bool:
        return sum(1 for a, b in zip(self.start, self.end) if a != b) == 1

# parse raw text into Lines
lines = tuple(
    Line(*(
        Point(map(int, point.split(",")))
        for point in line.split("->")
    ))
    for line in raw.strip().split("\n")
)

# create Point-to-count mapping
from collections import Counter
point_counts = Counter()
overlaps = lambda: sum(1 for count in point_counts.values() if count > 1)

# count points in horizontal and vertical lines
for points in (l.points() for l in lines if l.axis_aligned()):
    point_counts.update(points)
print(overlaps())

# count points in diagonal lines
for points in (l.points() for l in lines if not l.axis_aligned()):
    point_counts.update(points)
print(overlaps())
