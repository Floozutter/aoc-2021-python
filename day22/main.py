INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

import re
from typing import NamedTuple, Sequence

int_pattern = re.compile("-?[0-9]+")
class Instruction(NamedTuple):
    on: bool; x_min: int; x_max: int; y_min: int; y_max: int; z_min: int; z_max: int
    @classmethod
    def from_line(cls, line: str):
        l, r = line.strip().split()
        return cls(l == "on", *map(int, int_pattern.findall(r)))

def init(instructions: Sequence[Instruction]) -> frozenset[tuple[int, int, int]]:
    cubes: frozenset[tuple[int, int, int]] = frozenset()
    for i in instructions:
        region = {
            (x, y, z)
            for x in range(i.x_min, i.x_max+1)
            for y in range(i.y_min, i.y_max+1)
            for z in range(i.z_min, i.z_max+1)
        }
        if i.on:
            cubes |= region
        else:
            cubes -= region
    return cubes & {(x,y,z) for x in range(-50,51) for y in range(-50,51) for z in range(-50,51)}

instructions = tuple(map(Instruction.from_line, raw.strip().split("\n")))
print(len(init(instructions[:20])))
