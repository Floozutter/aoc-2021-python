INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
start1, start2 = (int(line.split()[-1]) for line in raw.strip().split("\n"))

def play_deterministic(start1: int, start2: int) -> int:
    spaces = [start1, start2]
    scores = [0, 0]
    rolls = 0
    while True:
        for i in (0, 1):
            spaces[i] = ((spaces[i]+3*rolls+6) - 1) % 10 + 1
            scores[i] += spaces[i]
            rolls += 3
            if scores[i] >= 1000:
                return rolls * scores[(i+1) % 2]
print(play_deterministic(start1, start2))

from functools import cache
@cache
def play_dirac(space1: int, score1: int, space2: int, score2: int) -> tuple[int, int]:
    if score1 >= 21:
        return (1, 0)
    elif score2 >= 21:
        return (0, 1)
    else:
        wins1 = wins2 = 0
        for outcome in (a+b+c for a in (1,2,3) for b in (1,2,3) for c in (1,2,3)):
            now1 = ((space1+outcome) - 1) % 10 + 1
            d2, d1 = play_dirac(space2, score2, now1, score1 + now1)
            wins1 += d1
            wins2 += d2
        return wins1, wins2
print(max(play_dirac(start1, 0, start2, 0)))
