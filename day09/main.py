INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
heightmap = tuple(tuple(map(int, row)) for row in raw.strip().split())
adjacents = lambda i, j: (
    (i+di, j+dj)
    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1))
    if 0 <= i+di < len(heightmap) and 0 <= j+dj < len(heightmap[0])
)
lows = []
for i, row in enumerate(heightmap):
    for j, h in enumerate(row):
        if all(
            heightmap[i][j] < heightmap[r][c]
            for r, c in adjacents(i, j)
        ):
            lows.append((i, j))
print(sum(heightmap[i][j] for i, j in lows) + len(lows))

def basin(i, j, visited) -> int:
    size = 1
    for r, c in adjacents(i, j):
        if (r, c) not in visited and heightmap[r][c] > heightmap[i][j] and heightmap[r][c] != 9:
            visited.add((r, c))
            size += basin(r, c, visited)
    return size
sizes = sorted(basin(i, j, set()) for i, j in lows)
print(sizes[-1]*sizes[-2]*sizes[-3])
