INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
Snumber = int | tuple["Snumber", "Snumber"]
def parse(s: str) -> Snumber:
    if s.isdecimal():
        return int(s)
    else:
        inner = s[1:-1]
        depth = 0
        for i, c in enumerate(inner):
            if c == "," and depth == 0:
                break
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
        l, r = inner[:i], inner[i+1:]
        return (parse(l), parse(r))
snumbers = tuple(map(parse, raw.strip().split()))

def height(sn: Snumber) -> int:
    if isinstance(sn, int):
        return 0
    else:
        l, r = sn
        return 1 + max((height(l), height(r)))
import re
p = re.compile("[0-9]+")
def helper(sn: Snumber) -> Snumber:
    s = str(sn).replace(" ", "").replace("(", "[").replace(")", "]")
    #print(s)
    depth = 0
    exploder = None
    for i, c in enumerate(s):
        if c == "[":
            depth += 1
            if depth > 4:
                exploder = i
                break
        elif c == "]":
            depth -= 1
    if exploder is not None:
        depth = 0
        for i, c in enumerate(s[exploder:]):
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    size = i
                    break
        es = s[exploder: exploder + size + 1]
        esn = parse(es)
        l, r = esn
        # handle left increase
        a = s[:exploder]
        matches = tuple(p.finditer(a))
        if matches:
            m = matches[-1]
            a = a[:m.start()] + str(int(a[m.start(): m.end()]) + l) + a[m.end():]
        # handle right increase
        b = s[exploder + size + 1:]
        matches = tuple(p.finditer(b))
        if matches:
            m = matches[0]
            b = b[:m.start()] + str(int(b[m.start(): m.end()]) + r) + b[m.end():]
        # combine
        rs = a + "0" + b
        return parse(rs)
    # split
    matches = tuple(p.finditer(s))
    for m in matches:
        n = int(s[m.start(): m.end()])
        if n >= 10:
            replacement = f"[{n//2},{-(n//-2)}]"
            ss = s[:m.start()] + replacement + s[m.end():]
            return parse(ss)
    return sn
def reduce(sn: Snumber) -> Snumber:
    reduced = helper(sn)
    while reduced != sn:
        sn, reduced = reduced, helper(reduced)
    return reduced

def magnitude(sn: Snumber) -> int:
    if isinstance(sn, int):
        return sn
    else:
        l, r = sn
        return 3*magnitude(l) + 2*magnitude(r)

from functools import reduce as fold
print(magnitude(fold(lambda a, b: reduce((a, b)), snumbers)))

from itertools import combinations
pairs = combinations(snumbers, 2)
actual = (a for pair in pairs for a in (lambda p: (p, (p[1], p[0])))(pair))
magnitudes = (magnitude(reduce((a, b))) for a, b in actual)
print(max(magnitudes))
