INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
header, *body = raw.strip().split("\n\n")

draws = tuple(map(int, header.split(",")))

class Board:
    def __init__(self, s: str):
        values = []
        for row in s.strip().split("\n"):
            values.append([int(n) for n in row.strip().split()])
        self.rows = values
    def won(self, numbers: set[int]) -> bool:
        for r in self.rows:
            if all(n in numbers for n in r):
                return True
        for c in tuple(map(tuple, zip(*self.rows))):
            if all(n in numbers for n in c):
                return True
        return False
    def unmarked(self, numbers: set[int]) -> int:
        return sum(
            sum(n for n in r if n not in numbers)
            for r in self.rows
        )
boards = tuple(map(Board, body))

def a():
    for i in range(1, len(draws) + 1):
        for b in boards:
            if b.won(set(draws[:i])):
                return b.unmarked(set(draws[:i])) * draws[i-1]
print(a())

def b(boards, draws, it):
    if len(boards) <= 1:
        last = boards[0]
        for d in it:
            draws.add(d)
            if last.won(draws):
                return last.unmarked(draws) * d
    else:
        draws.add(next(it))
        return b(tuple(x for x in boards if not x.won(draws)), draws, it)
print(b(boards, set(), iter(draws)))
