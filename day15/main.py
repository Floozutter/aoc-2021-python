INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
risks = tuple(tuple(map(int, row)) for row in raw.strip().split())
cavern1 = {(i, j): risk for i, row in enumerate(risks) for j, risk in enumerate(row)}
h, w = len(risks), len(risks[0])
cavern2 = {
    (i, j): ((risks[i%h][j%w] + (i//h) + (j//w)) - 1) % 9 + 1
    for i in range(5 * h)
    for j in range(5 * w)
}

import heapq
from typing import NamedTuple, Mapping

class RiskedPostion(NamedTuple):
    risk: int
    position: tuple[int, int]

def dijk(
    cavern: Mapping[tuple[int, int], int],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int | None:
    lowest_risk = {start: 0}
    frontier = [RiskedPostion(0, start)]
    while frontier:
        front = heapq.heappop(frontier)
        if front.position == end:
            return front.risk
        if lowest_risk[front.position] < front.risk:
            continue
        i, j = front.position
        for adj in (
            RiskedPostion(front.risk + cavern[p], p)
            for p in ((i-1, j), (i+1, j), (i, j-1), (i, j+1))
            if p in cavern
        ):
            if adj.position not in lowest_risk or adj.risk < lowest_risk[adj.position]:
                heapq.heappush(frontier, adj)
                lowest_risk[adj.position] = adj.risk
    return None

print(dijk(cavern1, (0, 0), (h - 1, w - 1)))
print(dijk(cavern2, (0, 0), (5*h - 1, 5*w - 1)))
