INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
initial = tuple(map(int, raw.strip().split(",")))

"""
def update(state):
    new = []
    end = []
    for x in state:
        x = x - 1
        if x == -1:
            x = 6
            end.append(8)
        new.append(x)
    return tuple(new + end)
state = initial
print(state)
for i in range(256):
    state = update(state)
    #print(state)
print(len(state))
"""

from functools import cache
@cache
def fish(timer: int, days: int) -> int:
    count = 1
    for i in range(1, days+1):
        timer -= 1
        if timer < 0:
            timer = 6
            count += fish(8, days - i)
    return count
print(sum(fish(x, 80) for x in initial))
print(sum(fish(x, 256) for x in initial))
