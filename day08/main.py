INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
    raw = ifile.read()
lines = (
    (
        tuple(frozenset(digit) for digit in value.strip().split())
        for value in line.split("|")
    )
    for line in raw.strip().split("\n")
)
inputs, outputs = zip(*lines)

print(sum(
    1
    for value in outputs
    for digit in value
    if len(digit) in {2, 4, 3, 7}
))

segments_to_digit = {
    frozenset("abcefg") : 0,
    frozenset("cf")     : 1,
    frozenset("acdeg")  : 2,
    frozenset("acdfg")  : 3,
    frozenset("bcdf")   : 4,
    frozenset("abdfg")  : 5,
    frozenset("abdefg") : 6,
    frozenset("acf")    : 7,
    frozenset("abcdefg"): 8,
    frozenset("abcdfg") : 9,
}
from collections.abc import Iterable, Mapping, Set
def solve_decoder(encoded_digits: Iterable[Set[str]]) -> Mapping[str, str]:
    # initialize unsolved encoder (mapping of unencoded segments to sets of possible encodings)
    encoder = {segment: set("abcdefg") for segment in "abcdefg"}
    # use number of segments in each encoded digit to partially solve encoder
    for encoded_digit in encoded_digits:
        n = len(encoded_digit)
        possible_digits = tuple(s for s in segments_to_digit.keys() if len(s) == n)
        # involved segments must encode to a segment in the encoded digit
        for involved in (s for s in "abcdefg" if all(s in d for d in possible_digits)):
            encoder[involved].intersection_update(encoded_digit)
        # uninvolved segments cannot encode to a segment in the encoded digit
        for uninvolved in (s for s in "abcdefg" if all(s not in d for d in possible_digits)):
            encoder[uninvolved].difference_update(encoded_digit)
    # filter out known mappings from each set of choices until solved
    while any(len(choices) > 1 for choices in encoder.values()):
        solved_choices = frozenset(
            next(iter(choices))
            for choices in encoder.values()
            if len(choices) == 1
        )
        for choices in encoder.values():
            if len(choices) > 1:
                choices.difference_update(solved_choices)
    # invert encoder for decoder
    return {next(iter(e)): d for d, e in encoder.items()}
def decode_digits(decoder: Mapping[str, str], digits: Iterable[Set[str]]) -> int:
    return int("".join(
        str(segments_to_digit[frozenset(decoder[e] for e in encoded_segments)])
        for encoded_segments in digits
    ))
print(sum(
    decode_digits(solve_decoder(i + o), o)
    for i, o in zip(inputs, outputs)
))
