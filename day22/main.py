INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

import re
from typing import NamedTuple, Iterable

class Cuboid(NamedTuple):
    x_min: int; x_max: int; y_min: int; y_max: int; z_min: int; z_max: int
    def volume(self) -> int:
        return (self.x_max+1-self.x_min) * (self.y_max+1-self.y_min) * (self.z_max+1-self.z_min)

int_pattern = re.compile("-?[0-9]+")
class Instruction(NamedTuple):
    on: bool
    cuboid: Cuboid
    @classmethod
    def from_line(cls, line: str):
        l, r = line.strip().split()
        return cls(l == "on", Cuboid(*map(int, int_pattern.findall(r))))

def update(state: tuple[Cuboid, ...], instructions: Iterable[Instruction]) -> tuple[Cuboid, ...]:
    return ()

instructions = tuple(map(Instruction.from_line, raw.strip().split("\n")))
inits = next(j for j, inst in enumerate(instructions) if any(abs(z) > 50 for z in inst.cuboid))
reactor: tuple[Cuboid, ...] = ()

for inst in instructions[:inits]: reactor = update(reactor, inst)
print(sum(cuboid.volume() for cuboid in reactor))

for inst in instructions[inits:]: reactor = update(reactor, inst)
print(sum(cuboid.volume() for cuboid in reactor))
