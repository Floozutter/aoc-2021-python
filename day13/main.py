INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
body, footer = raw.strip().split("\n\n")

from typing import NamedTuple
class Dot(NamedTuple): x: int; y: int
class Line(NamedTuple): axis: str; value: int

initial: frozenset[Dot] = frozenset(
    Dot(*map(int, line.split(",")))
    for line in body.strip().split()
)
lines: tuple[Line, ...] = tuple(
    Line(l[-1], int(r))
    for l, r in (line.split("=") for line in footer.strip().split("\n"))
)

def fold(dots: frozenset[Dot], line: Line) -> frozenset[Dot]:
    return frozenset(
        Dot(line.value - abs(d.x - line.value), d.y) if line.axis == "x" else
        Dot(d.x, line.value - abs(d.y - line.value))
        for d in dots
    )

dots = fold(initial, lines[0])
print(len(dots))

from functools import reduce
dots = reduce(fold, lines[1:], dots)
xs, ys = zip(*dots)
print("\n".join(
    "".join(
        "#" if (x, y) in dots else " "
        for x in range(min(xs), max(xs)+1)
    )
    for y in range(min(ys), max(ys)+1)
))
