INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
depths = tuple(map(int, raw.strip().split()))

number_of_increases = lambda seq: sum(1 for l, r in zip(seq, seq[1:]) if l < r)

print(number_of_increases(depths))
print(number_of_increases(tuple(
    sum(window) for window in zip(depths, depths[1:], depths[2:])
)))
