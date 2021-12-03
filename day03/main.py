INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
report = tuple(raw.strip().split())
columns = tuple(map(tuple, zip(*report)))

from statistics import mode
gamma_bits = "".join(mode(bits) for bits in columns)
epsilon_bits = "".join("0" if b == "1" else "1" for b in gamma_bits)
print(int(gamma_bits, 2) * int(epsilon_bits, 2))

numbers = set(report)
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
numbers = set(report)
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
