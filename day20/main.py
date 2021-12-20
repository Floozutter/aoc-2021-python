INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
header, body = raw.strip().split("\n\n")
alg = tuple(c == "#" for c in header)
inp = {(i, j) for i, r in enumerate(body.strip().split()) for j, c in enumerate(r) if c == "#"}

from collections.abc import Callable
Image = Callable[[int, int], bool]

from functools import cache
def enhance(src: Image) -> Image:
    @cache
    def get_pixel(i: int, j: int) -> bool:
        bits = "".join("1" if src(i + di, j + dj) else "0" for di in (-1,0,1) for dj in (-1,0,1))
        index = int(bits, 2)
        return alg[index]
    return get_pixel

def lit(img: Image, bounds: tuple[tuple[int, int], tuple[int, int]]) -> int:
    (im, ix), (jm, jx) = bounds
    return sum(1 for i in range(im, ix+1) for j in range(jm, jx+1) if img(i, j))

img = lambda i, j: (i, j) in inp
indices, jndices = zip(*inp)
bounds = ((min(indices), max(indices)), (min(jndices), max(jndices)))

for _ in range(2):
    img = enhance(img)
    bounds = ((bounds[0][0]-1, bounds[0][1]+1), (bounds[1][0]-1, bounds[1][1]+1))
print(lit(img, bounds))

for _ in range(48):
    img = enhance(img)
    bounds = ((bounds[0][0]-1, bounds[0][1]+1), (bounds[1][0]-1, bounds[1][1]+1))
print(lit(img, bounds))
