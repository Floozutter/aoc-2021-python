INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
hmap = tuple(tuple(map(int, row)) for row in raw.strip().split())
adjacents = lambda i, j: (
    (r, c) for r, c in ((i-1, j), (i+1, j), (i, j-1), (i, j+1))
    if 0 <= r < len(hmap) and 0 <= c < len(hmap[0])
)

lows = tuple(
    (i, j) for i, row in enumerate(hmap) for j, h in enumerate(row)
    if all(h < hmap[r][c] for r, c in adjacents(i, j))
)
print(sum(hmap[i][j] + 1 for i, j in lows))

from functools import reduce
def basin(i: int, j: int) -> frozenset[tuple[int, int]]:
    return reduce(
        lambda a, b: a | b,
        (basin(r, c) for r, c in adjacents(i, j) if hmap[r][c] > hmap[i][j] and hmap[r][c] != 9),
        frozenset(((i, j),))
    )
sizes = tuple(len(basin(*l)) for l in lows)
print(reduce(lambda a, b: a * b, sorted(sizes, reverse = True)[:3]))
