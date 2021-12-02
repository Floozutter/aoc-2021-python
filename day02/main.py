INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

h, d = 0, 0
for word, num in (s.split() for s in raw.strip().split("\n")):
    n = int(num)
    if word == "forward":
        h += n
    elif word == "down":
        d += n
    elif word == "up":
        d -= n
print(h * d)

h, d, aim = 0, 0, 0
for word, num in (s.split() for s in raw.strip().split("\n")):
    n = int(num)
    if word == "forward":
        h += n
        d += n * aim
    elif word == "down":
        aim += n
    elif word == "up":
        aim -= n
print(h * d)
