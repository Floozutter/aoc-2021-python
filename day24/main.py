INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

from typing import NamedTuple
class Instruction(NamedTuple):
    op: str
    a: str
    b: str | None = None

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

program = tuple(Instruction(*line.split()) for line in raw.strip().split("\n"))
print(next(
    n for n in range(99999999999999, 11111111111110, -1)
    if "0" not in str(n) and run(program, map(int, str(n)))["z"] == 0
))
