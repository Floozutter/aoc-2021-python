INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
body, footer = raw.strip().split("\n\n")

initial = frozenset(
    tuple(map(int, line.split(",")))
    for line in body.strip().split()
)

from typing import NamedTuple
class Fold(NamedTuple):
    coord: str
    value: int
    @classmethod
    def from_line(cls, line: str):
        l, r = line.split("=")
        return cls(l[-1], int(r))
folds = tuple(map(Fold.from_line, footer.strip().split("\n")))

def apply_fold(dots: frozenset[tuple[int, int]], fold: Fold) -> frozenset[tuple[int, int]]:
    new = set()
    for x, y in dots:
        if fold.coord == "y":
            if y >= fold.value:
                new.add((x, fold.value - (y - fold.value)))
            else:
                new.add((x, y))
        elif fold.coord == "x":
            if x >= fold.value:
                new.add((fold.value - (x - fold.value), y))
            else:
                new.add((x, y))
    return frozenset(new)

dots = frozenset(initial)
for fold in folds:
    dots = apply_fold(dots, fold)

for i in range(50, -10, -1):
    for j in range(-10, 10):
        print("#" if (i, j) in dots else ".", end="")
    print()

print(len(apply_fold(initial, folds[0])))
