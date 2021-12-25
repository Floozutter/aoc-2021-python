INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

from typing import NamedTuple
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

class Literal(NamedTuple): val: int
class Parameter(NamedTuple): idx: int
class Operation(NamedTuple): op: str; a: "Expression"; b: "Expression"
Expression = Literal | Parameter | Operation

from itertools import count
def transform(program: Iterable[Instruction]) -> dict[str, Expression]:
    mem: dict[str, Expression] = {name: Literal(0) for name in "wxyz"}
    indices = count()
    for op, a, b in program:
        if op == "inp":
            mem[a] = Parameter(next(indices))
        else:
            l = mem[a]
            r = mem[b] if b in mem else Literal(int(cast(str, b)))
            mem[a] = Operation(op, l, r)
    return mem

def print_tree(exp: Expression, pre: str = "", last: bool = True) -> str:
    print(f"{pre}{'└' if last else '├'}", end="")
    if isinstance(exp, Literal):
        print(exp.val)
    elif isinstance(exp, Parameter):
        print(exp.idx)
    else:
        print(exp.op)
        nextpre = pre + (" " if last else "│")
        print_tree(exp.a, nextpre, False)
        print_tree(exp.b, nextpre, True)

program = tuple(Instruction(*line.split()) for line in raw.strip().split("\n"))

"""
print(next(
    n for n in range(99999999999999, 11111111111110, -1)
    if "0" not in str(n) and run(program, map(int, str(n)))["z"] == 0
))
"""

exps = transform(program)
print_tree(exps["z"])
