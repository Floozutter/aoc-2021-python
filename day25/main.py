INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
sea = {(i, j): c for i, row in enumerate(raw.strip().split()) for j, c in enumerate(row)}
ix, jx = (value + 1 for value in max(sea))

def step(sea: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    posteast = {p: c if c != ">" else "." for p, c in sea.items()} | {
        (i, (j+1)%jx) if sea[i, (j+1)%jx] == "." else (i, j): e
        for (i, j), e in sea.items() if e == ">"
    }
    postsouth = {p: c if c != "v" else "." for p, c in posteast.items()} | {
        ((i+1)%ix, j) if posteast[(i+1)%ix, j] == "." else (i, j): e
        for (i, j), e in posteast.items() if e == "v"
    }
    return postsouth

i = 0
last = sea.copy()
while True:
    i += 1
    now = step(last)
    if now == last:
        break
    last = now
print(i)
