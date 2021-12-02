INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()

def parse_command(line: str) -> tuple[str, int]:
    word, n = line.split()
    return word, int(n)
commands = tuple(map(parse_command, raw.strip().split("\n")))

h = d = 0
for word, n in commands:
    match word:
        case "forward":
            h += n
        case "down":
            d += n
        case "up":
            d -= n
print(h * d)

h = d = aim = 0
for word, n in commands:
    match word:
        case "forward":
            h += n
            d += n * aim
        case "down":
            aim += n
        case "up":
            aim -= n
print(h * d)
