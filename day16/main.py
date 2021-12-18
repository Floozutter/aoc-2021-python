INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
bits = "".join(f"{int(h, 16):04b}" for h in raw.strip())

"""
to-do: refactor using queue instead of generator
"""

from typing import Iterator, TypeVar
T = TypeVar("T")
def exact_slice(it: Iterator[T], n: int) -> Iterator[T]:
    eager = tuple(next(it) for _ in range(n))
    return iter(eager)

from math import prod
from typing import NamedTuple
class Packet(NamedTuple):
    ver: int
    tid: int
    val: int | tuple["Packet", ...]
    @classmethod
    def parse(cls, it: Iterator[str]) -> "Packet":
        ver = int("".join(exact_slice(it, 3)), 2)
        tid = int("".join(exact_slice(it, 3)), 2)
        if tid == 4:
            l = []
            while True:
                head, *tail = "".join(exact_slice(it, 5))
                l.extend(tail)
                if head == "0":
                    return Packet(ver, tid, int("".join(l), 2))
        else:
            if next(it) == "0":
                size = int("".join(exact_slice(it, 15)), 2)
                sub_it = exact_slice(it, size)
                sub_packets = []
                try:
                    while True:
                        sub_packets.append(cls.parse(sub_it))
                except RuntimeError:  # StopIteration
                    return Packet(ver, tid, tuple(sub_packets))
            else:
                n = int("".join(exact_slice(it, 11)), 2)
                return Packet(ver, tid, tuple(cls.parse(it) for _ in range(n)))
    def vsum(self) -> int:
        return self.ver + (sum(s.vsum() for s in self.val) if isinstance(self.val, tuple) else 0)
    def eval(self) -> int:
        if self.tid == 0:
            return sum(s.eval() for s in self.val)
        elif self.tid == 1:
            return prod(s.eval() for s in self.val)
        elif self.tid == 2:
            return min(s.eval() for s in self.val)
        elif self.tid == 3:
            return max(s.eval() for s in self.val)
        elif self.tid == 4:
            return self.val
        elif self.tid == 5:
            return int(self.val[0].eval() > self.val[1].eval())
        elif self.tid == 6:
            return int(self.val[0].eval() < self.val[1].eval())
        elif self.tid == 7:
            return int(self.val[0].eval() == self.val[1].eval())
        else:
            raise AssertionError()

head = Packet.parse(iter(bits))
#print(head)
print(head.vsum())
print(head.eval())
