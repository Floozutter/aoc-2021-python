INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
template, body = raw.strip().split("\n\n")
rules = dict(line.split(" -> ") for line in body.strip().split("\n"))

from collections import Counter
def step(elements: Counter[str], pairs: Counter[str]) -> tuple[Counter[str], Counter[str]]:
    stepped_elements = elements.copy()
    stepped_pairs: Counter[str] = Counter()
    for pair, count in pairs.items():
        if pair in rules:
            l, r = tuple(pair)
            m = rules[pair]
            stepped_elements[m] += count
            stepped_pairs[l + m] += count
            stepped_pairs[m + r] += count
        else:
            stepped_pairs[pair] += count
    return stepped_elements, stepped_pairs

elements = Counter(template)
pairs = Counter(l + r for l, r in zip(template, template[1:]))
diff = lambda: elements.most_common()[0][1] - elements.most_common()[-1][1]
for _ in range(10): elements, pairs = step(elements, pairs)
print(diff())
for _ in range(30): elements, pairs = step(elements, pairs)
print(diff())
