INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
xs = tuple(map(int, raw.strip().split(",")))

from statistics import median
m = int(median(xs))
print(sum(abs(m - x) for x in xs))

t = lambda n: n*(n+1)//2
print(min(
    sum(t(abs(i - x)) for x in xs)
    for i in range(min(xs), max(xs) + 1)
))
