INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

import re
from typing import final, NamedTuple, Optional, Sequence

@final
class Cuboid(NamedTuple):
    x_min: int; x_max: int; y_min: int; y_max: int; z_min: int; z_max: int
    def degenerate(self: "Cuboid") -> bool:
        return self.x_min > self.x_max or self.y_min > self.y_max or self.z_min > self.z_max
    def __and__(self: "Cuboid", other: "Cuboid") -> Optional["Cuboid"]:
        cuboid = Cuboid(
            x_min = max(self.x_min, other.x_min),
            x_max = min(self.x_max, other.x_max),
            y_min = max(self.y_min, other.y_min),
            y_max = min(self.y_max, other.y_max),
            z_min = max(self.z_min, other.z_min),
            z_max = min(self.z_max, other.z_max),
        )
        return None if cuboid.degenerate() else cuboid
    def __sub__(self: "Cuboid", other: "Cuboid") -> tuple["Cuboid", ...]:
        intersection = self & other
        if intersection is None:
            return (self,)
        else:
            # for each axis of the cuboid find and sort all coordinates contained within the axis
            contained_xs = sorted(filter(
                lambda x: self.x_min <= x <= self.x_max,
                {self.x_min, self.x_max, other.x_min, other.x_max}
            ))
            contained_ys = sorted(filter(
                lambda y: self.y_min <= y <= self.y_max,
                {self.y_min, self.y_max, other.y_min, other.y_max}
            ))
            contained_zs = sorted(filter(
                lambda z: self.z_min <= z <= self.z_max,
                {self.z_min, self.z_max, other.z_min, other.z_max}
            ))
            # get nonoverlapping partitions that span each axis of the cuboid from adjacent coords
            p = Cuboid.partition_without_duplicate_endpoints
            x_partitions = p(contained_xs, keep_exact = (intersection.x_min, intersection.x_max))
            y_partitions = p(contained_ys, keep_exact = (intersection.y_min, intersection.y_max))
            z_partitions = p(contained_zs, keep_exact = (intersection.z_min, intersection.z_max))
            # get every nonoverlapping subcuboid of the minuend from every partition triple
            subcuboids = tuple(
                Cuboid(x_min, x_max, y_min, y_max, z_min, z_max)
                for x_min, x_max in x_partitions
                for y_min, y_max in y_partitions
                for z_min, z_max in z_partitions
            )
            # filter out the intersection subcuboid to keep only the subcuboids of the difference
            return tuple(filter(lambda cuboid: cuboid != intersection, subcuboids))
    def volume(self: "Cuboid") -> int:
        return (self.x_max+1-self.x_min) * (self.y_max+1-self.y_min) * (self.z_max+1-self.z_min)
    @staticmethod
    def partition_without_duplicate_endpoints(
        endpoints: Sequence[int],
        keep_exact: tuple[int, int],
    ) -> Sequence[tuple[int, int]]:
        if keep_exact[0] == keep_exact[1]:
            q = p = next(i for i, e in enumerate(endpoints) if e == keep_exact[0])
        else:
            p = next(i for i, p in enumerate(zip(endpoints, endpoints[1:])) if p == keep_exact)
            q = p + 1
        head = tuple((endpoints[i], endpoints[i+1] - 1) for i in range(p))
        tail = tuple((endpoints[i] + 1, endpoints[i+1]) for i in range(q, len(endpoints) - 1))
        return head + (keep_exact,) + tail

int_pattern = re.compile("-?[0-9]+")
class Instruction(NamedTuple):
    on: bool
    cuboid: Cuboid
    @classmethod
    def from_line(cls, line: str):
        l, r = line.strip().split()
        return cls(l == "on", Cuboid(*map(int, int_pattern.findall(r))))

def update(state: tuple[Cuboid, ...], instruction: Instruction) -> tuple[Cuboid, ...]:
    difference = tuple(subcuboid for cuboid in state for subcuboid in cuboid - instruction.cuboid)
    return difference + ((instruction.cuboid,) if instruction.on else ())

instructions = tuple(map(Instruction.from_line, raw.strip().split("\n")))
inits = next(j for j, inst in enumerate(instructions) if any(abs(z) > 50 for z in inst.cuboid))
reactor: tuple[Cuboid, ...] = ()

for inst in instructions[:inits]: reactor = update(reactor, inst)
print(sum(cuboid.volume() for cuboid in reactor))

for inst in instructions[inits:]: reactor = update(reactor, inst)
print(sum(cuboid.volume() for cuboid in reactor))
