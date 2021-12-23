INPUTPATH = "input.txt"
INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
rows = raw.strip().split("\n")

spaces = frozenset((i, j) for i, r in enumerate(rows) for j, c in enumerate(r) if c in ".ABCD")
entrances = frozenset(((1, 3), (1, 5), (1, 7), (1, 9)))
rooms = {
    "A": frozenset(((2, 3), (3, 3))),
    "B": frozenset(((2, 5), (3, 5))),
    "C": frozenset(((2, 7), (3, 7))),
    "D": frozenset(((2, 9), (3, 9))),
}
hallway = spaces - frozenset(p for r in rooms.values() for p in r)
costs = {"A": 1, "B": 10, "C": 100, "D": 1000}

import heapq
from itertools import permutations
from functools import cache
from typing import NamedTuple

def adjacents(pos: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    return tuple((pos[0]+di, pos[1]+dj) for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)))

@cache
def shortest_distance(start: tuple[int, int], end: tuple[int, int]) -> int:
    shortest_distances = {start: 0}
    frontier = [(0, start)]
    while frontier:
        d, pos = heapq.heappop(frontier)
        if pos == end:
            return d
        if d > shortest_distances[pos]:
            continue
        for adj in adjacents(pos):
            if adj in spaces:
                dd = d + 1
                if adj not in shortest_distances or dd < shortest_distances[adj]:
                    heapq.heappush(frontier, (dd, adj))
                    shortest_distances[adj] = dd
    raise ValueError

class Amphipod(NamedTuple):
    kind: str
    pos: tuple[int, int]

class AmphiState(NamedTuple):
    amphipods: frozenset[Amphipod]
    @cache
    def heuristic(self) -> int:
        total = 0
        for kind in "ABCD":
            amphipods = tuple(a for a in self.amphipods if a.kind == kind)
            homes = tuple(rooms[kind])
            total += costs[kind] * min(
                sum(shortest_distance(a.pos, home) for a, home in zip(perm, homes))
                for perm in permutations(amphipods)
            )
        return total

class Exploration(NamedTuple):
    expected: int
    energy: int
    state: AmphiState

def least_energy_required(start: AmphiState) -> int:
    least_energies = {start: 0}
    frontier = [Exploration(start.heuristic(), 0, start)]
    while frontier:
        front = heapq.heappop(frontier)
        print(front[:2])
        if all(a in rooms[a.kind] for a in front.state.amphipods):
            return front.energy
        if front.energy > least_energies[front.state]:
            continue
        for mover in front.state.amphipods:
            others = front.state.amphipods - {mover}
            for moved in (
                Amphipod(mover.kind, adj) for adj in adjacents(mover.pos)
                if adj in spaces and not any(o.pos == adj for o in others)
            ):
                energy = front.energy + costs[moved.kind]
                state = AmphiState(others | {moved})
                if state not in least_energies or energy < least_energies[state]:
                    heapq.heappush(frontier, Exploration(energy+state.heuristic(), energy, state))
                    least_energies[state] = energy
    raise ValueError

print(least_energy_required(AmphiState(frozenset(
    Amphipod(c, (i, j))
    for i, r in enumerate(rows) for j, c in enumerate(r)
    if c in "ABCD"
))))
