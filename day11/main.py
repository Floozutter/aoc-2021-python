INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
ini = tuple(map(int, raw.strip().split()))
d = {
    (i, j): int(n)
    for i, row in enumerate(raw.strip().split())
    for j, n in enumerate(row)
}

def step() -> int:
    for k in d:
        d[k] += 1
    flashed = set()
    while True:
        flashes = set((i, j) for i in range(10) for j in range(10) if d[i, j] > 9)
        if not flashes:
            return len(flashed)
        flashed.update(flashes)
        for i, j in flashes:
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if (i+di, j+dj) in d:
                        d[i+di, j+dj] += 1
        for f in flashed:
            d[f] = 0

count = 0
for i in range(100):
    count += step()
print(count)

d = {
    (i, j): int(n)
    for i, row in enumerate(raw.strip().split())
    for j, n in enumerate(row)
}
for i in range(1_000_000):
    x = step()
    #print(x)
    if x == 100:
        print(i+1)
        break
