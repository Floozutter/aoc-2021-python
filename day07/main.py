INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
ps = tuple(map(int, raw.strip().split(",")))
from statistics import median
m = int(median(ps))
print(sum(abs(m - p) for p in ps))

lowest = None
for i in range(min(ps), max(ps) + 1):
    cost = sum(
        sum(i+1 for i in range(abs(i - p)))
        for p in ps
    )
    if lowest is None or cost < lowest:
        lowest = cost
print(lowest)
