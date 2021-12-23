INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
rows = raw.strip().split("\n")

import heapq
from itertools import permutations
from functools import cache
from typing import NamedTuple, cast

Position = tuple[int, int]

class Burrow(NamedTuple):
    spaces: frozenset[Position]
    hall: frozenset[Position]
    rooms: dict[str, tuple[Position, ...]]

class Amphipod(NamedTuple): 
    kind: str
    pos: Position

def adjacents(pos: Position) -> tuple[Position, ...]:
    return tuple((pos[0]+di, pos[1]+dj) for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)))

@cache
def distance(positions: frozenset[Position], start: Position, end: Position) -> int | None:
    positions = frozenset(positions)
    if end not in positions: return None
    shortest_distances = {start: 0}
    frontier = [(0, start)]
    while frontier:
        d, pos = heapq.heappop(frontier)
        if pos == end:
            return d
        if d > shortest_distances[pos]:
            continue
        for adj in adjacents(pos):
            if adj in positions:
                dd = d + 1
                if adj not in shortest_distances or dd < shortest_distances[adj]:
                    heapq.heappush(frontier, (dd, adj))
                    shortest_distances[adj] = dd
    return None

STEPCOSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}
def least_energy_to_organize(burrow: Burrow, start: frozenset[Amphipod]) -> int | None:
    # define the possible transitions from a given configuration of amphipods
    @cache
    def next_home_in_room(state: frozenset[Amphipod], kind: str) -> Position | None:
        room = burrow.rooms[kind]
        if any(a.pos in room for a in state if a.kind != kind): return None
        occupied = {a.pos for a in state}
        return next(reversed(tuple(p for p in room if p not in occupied)), None)
    @cache
    def transitions(state: frozenset[Amphipod]) -> tuple[tuple[frozenset[Amphipod], int], ...]:
        # move any amphipod waiting in the hall to their room if possible
        for waiter in (a for a in front.state if a.pos in burrow.hall):
            home = next_home_in_room(front.state, waiter.kind)
            if home is not None:
                d = distance(burrow.spaces - {a.pos for a in front.state}, waiter.pos, home)
                if d is not None:
                    s = state - {waiter} | {Amphipod(waiter.kind, home)}
                    cost = STEPCOSTS[waiter.kind] * d
                    return ((frozenset(s), cost),)
        # move out amphipods that are in a room but not in their home to the hall
        ret = []
        for mover in (a for a in front.state if a.pos not in burrow.hall):
            k, room = next((k, r) for k, r in burrow.rooms.items() if mover.pos in r)
            if k != mover.kind or any(a.pos in room for a in state if a.kind != k):
                for pos in burrow.hall:
                    d = distance(burrow.spaces - {a.pos for a in front.state}, mover.pos, pos)
                    if d is not None:
                        s = state - {mover} | {Amphipod(mover.kind, pos)}
                        cost = STEPCOSTS[mover.kind] * d
                        ret.append((frozenset(s), cost))
        return tuple(ret)
    # helpers for A*
    @cache
    def heuristic(state: frozenset[Amphipod]) -> int:
        total = 0
        for kind in "ABCD":
            positions = tuple(a.pos for a in state if a.kind == kind)
            homes = burrow.rooms[kind]
            total += STEPCOSTS[kind] * min(
                sum(
                    cast(int, distance(burrow.spaces, p, h))
                    for p, h in zip(perm, homes)
                )
                for perm in permutations(positions)
            )
        return total
    class Exploration(NamedTuple):
        expected: int
        energy: int
        state: frozenset[Amphipod]
    # A* search over the graph of amphipod configurations in the burrow
    least_energies = {start: 0}
    frontier = [Exploration(heuristic(start), 0, frozenset(start))]
    while frontier:
        front = heapq.heappop(frontier)
        if all(a.pos in burrow.rooms[a.kind] for a in front.state):
            return front.energy
        if front.energy > least_energies[front.state]:
            continue
        for state, energycost in transitions(front.state):
            energy = front.energy + energycost
            if state not in least_energies or energy < least_energies[state]:
                heapq.heappush(frontier, Exploration(energy+heuristic(state), energy, state))
                least_energies[state] = energy
    return None

burrow1 = Burrow(
    spaces = frozenset((i,j) for i, r in enumerate(rows) for j, c in enumerate(r) if c in ".ABCD"),
    hall = frozenset((1, j) for j in range(1, 12)) - {(1, j) for j in (3,5,7,9)},
    rooms = {kind: tuple((i, j) for i in range(2, 4)) for j, kind in zip((3,5,7,9), "ABCD")},
)
amphipods1 = frozenset(
    Amphipod(c, (i, j)) for i, r in enumerate(rows) for j, c in enumerate(r) if c in "ABCD"
)
print(least_energy_to_organize(burrow1, amphipods1))

burrow2 = Burrow(
    spaces = burrow1.spaces | {(i, j) for i in range(4, 6) for j in (3,5,7,9)},
    hall = burrow1.hall,
    rooms = {kind: tuple((i, j) for i in range(2, 6)) for j, kind in zip((3,5,7,9), "ABCD")},
)
amphipods2 = frozenset(Amphipod(k, (2 if i == 2 else 5, j)) for k, (i, j) in amphipods1) | {
    Amphipod("D",(3,3)), Amphipod("C",(3,5)), Amphipod("B",(3,7)), Amphipod("A",(3,9)),
    Amphipod("D",(4,3)), Amphipod("B",(4,5)), Amphipod("A",(4,7)), Amphipod("C",(4,9)),
}
print(least_energy_to_organize(burrow2, amphipods2))
