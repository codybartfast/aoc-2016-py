#  Day 04
#  ======
#
#  Part 1: 361724
#  Part 2: 482
#
#  Timings
#  ---------------------
#    Parse:     0.000256
#   Part 1:     0.005761
#   Part 2:     0.000160
#  Elapsed:     0.006221


from itertools import groupby, islice
import string

CHARS = string.ascii_lowercase

translators = [
    str.maketrans(CHARS, CHARS[shift:] + CHARS[:shift]) for shift in range(26)
]


def parse(text):
    return [(line[:-11], int(line[-10:-7]), line[-6:-1]) for line in text.splitlines()]


def checksum(name):
    # Wasn't aware of Counter until I read other people's solutions after completing this
    groups = ((key, list(grpr)) for key, grpr in groupby(sorted(name)))
    by_freq = (
        char
        for char, _ in sorted(groups, key=lambda grp: (-len(grp[1]), grp[0]))
        if char != "-"
    )
    return "".join(islice(by_freq, 5))


def part1(rooms, args, state_for_part2):
    return sum(sect for encr, sect, csum in rooms if checksum(encr) == csum)


def part2(rooms, args, state_from_part1):
    for encr, sect, csum in rooms:
        # if checksum(encr) == csum:
        name = encr.translate(translators[sect % 26])
        if "north" in name:
            return sect


def jingle(filepath=None, text=None, extra_args=None):
    if not text and filepath:
        with open(filepath, "r") as f:
            text = f.read().strip()
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys
    import sack

    file = sys.argv[1] if len(sys.argv) > 1 else None
    filepath = sack.get_filepath(file)
    if filepath:
        extra_args = sys.argv[1:] if len(sys.argv) > 1 else []
        jingle(filepath=filepath, extra_args=extra_args)
