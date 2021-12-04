INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
header, *bodies = raw.strip().split("\n\n")

from typing import NamedTuple, Iterable, Optional, cast
class Win(NamedTuple):
    turn: int
    score: int
class Board:
    unmarked: set[int]
    axes: tuple[set[int], ...]
    def __init__(self, grid: Iterable[Iterable[int]]):
        rows = tuple(tuple(row) for row in grid)
        cols: tuple[tuple[int, ...], ...] = tuple(map(tuple, zip(*rows)))
        self.axes = tuple(map(set, rows + cols))
        self.unmarked = set(n for a in self.axes for n in a)
    def mark(self, number: int) -> bool:
        self.unmarked.discard(number)
        for a in self.axes:
            a.discard(number)
            if not a:
                return True
        return False
    def play(self, draws: Iterable[int]) -> Optional[Win]:
        for i, n in enumerate(draws):
            if self.mark(n):
                return Win(i + 1, sum(self.unmarked) * n)
        return None

draws = tuple(map(int, header.split(",")))
results = tuple(
    Board(map(int, r.strip().split()) for r in body.strip().split("\n")).play(draws)
    for body in bodies
)
assert all(isinstance(r, Win) for r in results)
wins = cast(Iterable[Win], results)
print(min(wins).score)
print(max(wins).score)
