INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
template, body = raw.strip().split("\n\n")
rules = {
    l: r
    for l, r in (line.split(" -> ") for line in body.strip().split("\n"))
}

def part1():
    def step(s: str) -> str:
        o = []
        for a, b in zip(s, s[1:]):
            o.append(a)
            if a+b in rules:
                o.append(rules[a+b])
        o.append(s[-1])
        return "".join(o)
    s = template
    for _ in range(10):
        #print(s)
        s = step(s)
    from collections import Counter
    counts = Counter(s).most_common()
    print(counts[0][1] - counts[-1][1])
part1()

def part2():
    from collections import Counter
    def step2(adjacencies, lol):
        x = Counter()
        lmao = lol.copy()
        for pair, count in adjacencies.items():
            if pair in rules:
                l, r = pair
                m = rules[pair]
                x[l+m] += count
                x[m+r] += count
                lmao[m] += count
            else:
                x[pair] += count
        return x, lmao
    owo = Counter()
    uwu = Counter(template)
    for a, b in zip(template, template[1:]):
        owo[a+b] += 1
    for _ in range(40):
        #print(owo, uwu)
        owo, uwu = step2(owo, uwu)
    counts = uwu.most_common()
    print(counts[0][1] - counts[-1][1])
part2()
