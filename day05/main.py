INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

def parse_line(s: str):
    l, r = s.split("->")
    a, b = l.split(",")
    c, d = r.split(",")
    return tuple(map(int, (a, b, c, d)))
lines = tuple(map(parse_line, raw.strip().split("\n")))
only = tuple((a, b, c, d) for a, b, c, d in lines if a == c or b == d)

from collections import Counter
counter = Counter()
for a, b, c, d in only:
    points = set()
    q, w = sorted((a, c))
    for x in range(q, w+1):
        points.add((x, b))
    e, r = sorted((b, d))
    for y in range(e, r+1):
        points.add((a, y))
    for p in points:
        counter[p] += 1
print(sum(1 for count in counter.values() if count >= 2))

counter = Counter()
for a, b, c, d in lines:
    points = set()
    if a == c or b == d:
        q, w = sorted((a, c))
        for x in range(q, w+1):
            points.add((x, b))
        e, r = sorted((b, d))
        for y in range(e, r+1):
            points.add((a, y))
    else:
        for i in range(abs(c - a) + 1):
            x = a + i if c > a else a - i
            y = b + i if d > b else b - i
            points.add((x, y))
    for p in points:
        counter[p] += 1
print(sum(1 for count in counter.values() if count >= 2))

"""
for x in range(10):
    for y in range(10):
        print(counter[y, x], end="")
    print("")
"""
