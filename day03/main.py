INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

data = tuple(raw.strip().split())

from collections import Counter

zeros = Counter()
ones = Counter()
for bitstring in data:
    for i, c in enumerate(bitstring):
        if c == "0":
            zeros[i] += 1
        else:
            ones[i] += 1
gamma = []
for i in range(len(data[0])):
    if zeros[i] > ones[i]:
        gamma.append("0")
    else:
        gamma.append("1")
gamma = "".join(gamma)
epsilon = "".join("0" if g == "1" else "1" for g in gamma)
gamma = int(gamma, 2)
epsilon = int(epsilon, 2)
print(gamma*epsilon)

numbers = set(data)
i = 0
while len(numbers) > 1:
    zeros = 0
    for n in numbers:
        if n[i] == "0":
            zeros += 1
    ones = len(numbers) - zeros
    for n in tuple(numbers):
        if n[i] == ("0" if ones >= zeros else "1"):
            numbers.remove(n)
    i += 1
o = int(next(iter(numbers)), 2)
numbers = set(data)
i = 0
while len(numbers) > 1:
    zeros = 0
    for n in numbers:
        if n[i] == "0":
            zeros += 1
    ones = len(numbers) - zeros
    for n in tuple(numbers):
        if n[i] == ("0" if ones < zeros else "1"):
            numbers.remove(n)
    i += 1
c = int(next(iter(numbers)), 2)
print(o*c)
