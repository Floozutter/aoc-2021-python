INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
lines = tuple(raw.strip().split())

brackets = {"(": ")", "[": "]", "{": "}", "<": ">"}
points_corrupted = {")": 3, "]": 57, "}": 1197, ">": 25137}
points_incomplete = {")": 1, "]": 2, "}": 3, ">": 4}

from typing import NamedTuple
class Corrupted(NamedTuple): score: int
class Incomplete(NamedTuple): score: int

from functools import reduce
def score(line: str) -> Corrupted | Incomplete | None:
    openers = []
    for b in line:
        if b in brackets:
            openers.append(b)
        elif not openers or b != brackets[openers[-1]]:
            return Corrupted(points_corrupted[b])
        else:
            openers.pop()
    if openers:
        return Incomplete(reduce(
            lambda total, closer: 5*total + points_incomplete[closer],
            (brackets[o] for o in reversed(openers)),
            0
        ))
    return None

scores = tuple(map(score, lines))
print(sum(c.score for c in scores if isinstance(c, Corrupted)))
from statistics import median_low
print(median_low(i.score for i in scores if isinstance(i, Incomplete)))
