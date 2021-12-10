INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
lines = tuple(raw.strip().split())

brackets = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

corrupted = []
for l in lines:
    stack = []
    for c in l:
        if c in brackets:
            stack.append(c)
        else:
            if not stack or c != brackets[stack[-1]]:
                corrupted.append(c)
                break
            else:
                stack.pop()
print(sum(points[c] for c in corrupted))

def score(l):
    stack = []
    for c in l:
        if c in brackets:
            stack.append(c)
        else:
            if not stack or c != brackets[stack[-1]]:
                return 0
            else:
                stack.pop()
    x = "".join(brackets[c] for c in reversed(stack))
    t = 0
    for c in x:
        t *= 5
        if c == ")":
            t += 1
        elif c == "]":
            t += 2
        elif c == "}":
            t += 3
        else:
            t += 4
    return t
scores = []
for l in lines:
    scores.append(score(l))
from statistics import median
print(int(median(s for s in scores if s)))
