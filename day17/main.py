INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
import re
a, b, c, d = map(int, re.findall("-?[0-9]+", raw))

def f(vx: int, vy: int) -> tuple[bool, int]:
    highest = x = y = 0
    while True:
        if y < c and vy <= 0:
            return False, highest
        if a <= x <= b and c <= y <= d:
            return True, highest
        x += vx
        y += vy
        if y > highest:
            highest = y
        vx += -1 if vx > 0 else +1 if vx < 0 else 0
        vy += -1

results = (f(vx, vy) for vx in range(0, b+1) for vy in range(c, 200))  # just guess lol
valid = tuple(r for r in results if r[0])
print(max(valid, key = lambda r: r[1]))
print(len(valid))
