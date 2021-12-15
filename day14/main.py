INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
template, body = raw.strip().split("\n\n")
rules = dict(line.split(" -> ") for line in body.strip().split("\n"))

from collections import Counter
from functools import cache
@cache
def expand_pair(l: str, r: str, n: int) -> Counter[str]:
    m = rules.get(l+r)
    if n <= 0 or m is None:
        return Counter((l, r))
    else:
        return expand_pair(l, m, n-1) + expand_pair(m, r, n-1) - Counter((m,))
def expand(polymer: str, n: int) -> Counter[str]:
    pairs = zip(polymer, polymer[1:])
    overlaps = polymer[1:-1]
    return sum((expand_pair(l, r, n) for l, r in pairs), Counter("")) - Counter(overlaps)

diff = lambda counter: counter.most_common()[0][1] - counter.most_common()[-1][1]
print(diff(expand(template, 10)))
print(diff(expand(template, 40)))
