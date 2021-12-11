INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
octopi = {(i, j): int(n) for i, row in enumerate(raw.strip().split()) for j, n in enumerate(row)}

from collections import Counter
def step(octopi: dict[tuple[int, int], int]) -> int:
    octopi.update({p: e+1 for p, e in octopi.items()})
    tired = set()
    while flashes := set(p for p, e in octopi.items() if e > 9):
        tired.update(flashes)
        octopi.update({p: 0 for p in flashes})
        adjacents = ((i+di, j+dj) for i, j in flashes for di in (-1, 0, 1) for dj in (-1, 0, 1))
        increases = Counter(adjacents).items()
        octopi.update({p: octopi[p]+i for p, i in increases if p in octopi and p not in tired})
    return len(tired)

count = 0
for i in range(100):
    count += step(octopi)
print(count)

while True:
    i += 1
    if step(octopi) >= 100:
        break
print(i + 1)
