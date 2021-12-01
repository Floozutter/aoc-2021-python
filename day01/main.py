INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
depths = tuple(map(int, raw.strip().split()))

print(sum(
    1 for last, curr in zip(depths, depths[1:])
    if last < curr
))

print(sum(
    1 for a, b, c, d in zip(*map(lambda i: depths[i:], range(4)))
    if a+b+c < b+c+d
))
