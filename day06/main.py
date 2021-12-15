INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
timers = tuple(map(int, raw.strip().split(",")))

from functools import cache
@cache
def total_fish(timer: int, days: int) -> int:
    if days <= 0:
        return 1
    elif timer <= 0:
        return total_fish(6, days - 1) + total_fish(8, days - 1)
    else:
        return total_fish(timer - 1, days - 1)

print(sum(total_fish(t, 80) for t in timers))
print(sum(total_fish(t, 256) for t in timers))
