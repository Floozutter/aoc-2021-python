INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
report = tuple(raw.strip().split())

columns = tuple(map(tuple, zip(*report)))
from statistics import mode
gamma_bits = "".join(mode(bits) for bits in columns)
epsilon_bits = "".join("0" if b == "1" else "1" for b in gamma_bits)
print(int(gamma_bits, 2) * int(epsilon_bits, 2))

from typing import Sequence, Callable
def find_rating(bitstrings: Sequence[str], criteria: Callable[[str], str], index: int = 0) -> int:
    if len(bitstrings) <= 1:
        return int(bitstrings[0], 2)
    else:
        keep = criteria("".join(s[index] for s in bitstrings))
        return find_rating(tuple(s for s in bitstrings if s[index] == keep), criteria, index + 1)
ceildiv = lambda n, d: -(n // -d)
oxy = find_rating(report, lambda col: "01"[col.count("1") >= ceildiv(len(col), 2)])
co2 = find_rating(report, lambda col: "01"[col.count("1")  < ceildiv(len(col), 2)])
print(oxy * co2)
