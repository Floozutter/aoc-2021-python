INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

from itertools import count
from typing import NamedTuple
from dataclasses import dataclass
from collections.abc import Sequence

class Instruction(NamedTuple): op: str; a: str; b: str | None = None

from typing import Iterable, cast
def run(program: Iterable[Instruction], inputs: Iterable[int]) -> dict[str, int]:
    mem = {name: 0 for name in "wxyz"}
    it = iter(inputs)
    for op, a, b in program:
        if op == "inp":
            mem[a] = next(it)
        else:
            l, r = mem[a], mem[b] if b in mem else int(cast(str, b))
            if   op == "add": mem[a] = l + r
            elif op == "mul": mem[a] = l * r
            elif op == "div": mem[a] = int(l / r)
            elif op == "mod": mem[a] = l % r
            elif op == "eql": mem[a] = int(l == r)
            else: raise ValueError
    return mem

@dataclass(frozen = True)
class Expression:
    def evaluate(self, params: Sequence[int]) -> int:
        if isinstance(self, Literal):
            return self.val
        elif isinstance(self, Parameter):
            return params[self.idx]
        else:
            assert isinstance(self, Operation)
            op, a, b = self.op, self.a.evaluate(params), self.b.evaluate(params)
            if   op == "add": return a + b
            elif op == "mul": return a * b
            elif op == "div": return int(a / b)
            elif op == "mod": return a % b
            elif op == "eql": return a == b
            else: raise ValueError
    def print_tree(self, pre: str = "", last: bool = True) -> None:
        print(f"{pre}{'└' if last else '├'}", end="")
        if isinstance(self, Literal):
            print(self.val)
        elif isinstance(self, Parameter):
            print(f"p[{self.idx}]")
        else:
            assert isinstance(self, Operation)
            print(self.op)
            nextpre = pre + (" " if last else "│")
            self.a.print_tree(nextpre, False)
            self.b.print_tree(nextpre, True)
@dataclass(frozen = True)
class Literal(Expression): val: int
@dataclass(frozen = True)
class Parameter(Expression): idx: int
@dataclass(frozen = True)
class Operation(Expression):
    op: str
    a: "Expression"
    b: "Expression"
    def simplify(self) -> Expression:
        op, a, b = self.op, self.a, self.b
        if isinstance(a, Literal) and isinstance(b, Literal):
            return Literal(self.evaluate(()))
        elif op == "add" and a == Literal(0):
            return b
        elif op == "add" and b == Literal(0):
            return a
        elif op == "mul" and (a == Literal(0) or b == Literal(0)):
            return Literal(0)
        elif op == "mul" and a == Literal(1):
            return b
        elif op == "mul" and b == Literal(1):
            return a
        elif op == "div" and a == Literal(0):
            return Literal(0)
        elif op == "div" and b == Literal(1):
            return a
        elif op == "div" and a == b:
            return Literal(1)
        elif op == "mod" and (a == Literal(0) or b == Literal(1) or a == b):
            return Literal(0)
        elif op == "eql" and a == b:
            return Literal(1)
        else:
            return Operation(op, a, b)

def transform(program: Iterable[Instruction]) -> dict[str, Expression]:
    mem: dict[str, Expression] = {name: Literal(0) for name in "wxyz"}
    indices = count()
    for op, a, b in program:
        if op == "inp":
            mem[a] = Parameter(next(indices))
        else:
            l = mem[a]
            r = mem[b] if b in mem else Literal(int(cast(str, b)))
            mem[a] = Operation(op, l, r).simplify()
    return mem

program = tuple(Instruction(*line.split()) for line in raw.strip().split("\n"))

"""
print(next(
    n for n in range(99999999999999, 11111111111110, -1)
    if "0" not in str(n) and run(program, map(int, str(n)))["z"] == 0
))
"""

exp = transform(program)["z"]
#exp.print_tree()
print(run(program, (9,)*14)["z"])
#print(exp.evaluate((9,)*14))



"""
import random
import heapq
best = [(-run(program, (9,)*14)["z"], (9,)*14)]*10
for _ in range(100_000):
    digits = tuple(random.randint(1, 9) for _ in range(14))
    z = run(program, digits)["z"]
    heapq.heappushpop(best, (-z, digits))
    print(digits, z)
    if z == 0:
        break
print(sorted(best))
"""

import random
best_z = run(program, [9]*14)["z"]
best_digits = [9]*14
while True:
    k = random.randint(1, 14)
    indices = random.sample(range(14), k)
    digits = best_digits.copy()
    for i in indices:
        digits[i] = random.randint(1, 9)
    if int("".join(map(str, digits))) <= 79197919193676:
        continue
    z = run(program, digits)["z"]
    if z == 0:
        break
    if z < best_z:
        print(best_digits, digits, best_z, z)
        best_z = z
        best_digits = digits
print("".join(map(str, best_digits)))

# not 13191617971545
# not 79197919182465
# not 79197919193676
# consider: 91471914682432 (16)
# consider: 81471914682432 (15)
