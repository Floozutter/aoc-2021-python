INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
inputs, outputs = zip(*(
    tuple(
        tuple(map(frozenset, half.strip().split()))
        for half in line.split("|")
    )
    for line in raw.strip().split("\n"))
)

print(sum(
    1
    for value in outputs
    for digit in value
    if len(digit) in {2, 4, 3, 7}
))

from typing import NamedTuple
from collections.abc import Set
class InvolvedSegments(NamedTuple):
    definitely: frozenset[str]
    impossible: frozenset[str]
    @classmethod
    def from_size(cls, size: int):
        c = lambda a, b: cls(frozenset(a), frozenset(b))
        match size:
            case 2:
                return c("cf", "abdeg")
            case 3:
                return c("acf", "bdeg")
            case 4:
                return c("bcdf", "aeg")
            case 5:
                return c("adg", "")
            case 6:
                return c("abfg", "")
            case 7:
                return c("abcdefg", "")
            case _:
                raise ValueError("impossible number of segments")

def digit_from_segments(segments: Set[str]) -> int:
    match "".join(sorted(segments)):
        case "abcefg":
            return 0
        case "cf":
            return 1
        case "acdeg":
            return 2
        case "acdfg":
            return 3
        case "bcdf":
            return 4
        case "abdfg":
            return 5
        case "abdefg":
            return 6
        case "acf":
            return 7
        case "abcdefg":
            return 8
        case "abcdfg":
            return 9
        case _:
            raise ValueError("invalid digit")

from itertools import chain
from collections.abc import Sequence
def decode(i: Sequence[Set[str]], o: Sequence[Set[str]]) -> int:
    mapping = {c: set("abcdefg") for c in "abcdefg"}
    for digit in chain(i, o):
        involved = InvolvedSegments.from_size(len(digit))
        for s in involved.definitely:
            mapping[s].intersection_update(digit)
        for s in involved.impossible:
            mapping[s].difference_update(digit)
    while any(len(choices) > 1 for choices in mapping.values()):
        if any(not choices for choices in mapping.values()):
            raise ValueError("impossible mapping of segments")
        solved = frozenset(
            next(iter(choices))
            for choices in mapping.values()
            if len(choices) == 1
        )
        for choices in mapping.values():
            if len(choices) > 1:
                choices.difference_update(solved)
    actual_mapping = {next(iter(v)): k for k, v in mapping.items()}
    return int("".join(
        str(digit_from_segments(
            actual_mapping[s]
            for s in encoded
        ))
        for encoded in o
    ))

print(sum(decode(i, o) for i, o in zip(inputs, outputs)))
