INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
data = tuple(map(int, raw.strip().split()))

count = 0
for i in range(len(data) - 1):
    if data[i] < data[i+1]:
        count += 1
print(count)

count2 = 0
for i in range(len(data) - 3):
    left, right = data[i:i+3], data[i+1:i+4]
    if sum(left) < sum(right):
        count2 += 1
print(count2)
