#  Day 16
#  ======
#
#  Part 1: 10100011010101011
#  Part 2: 01010001101011001
#
#  Timings
#  ---------------------
#    Parse:     0.000002
#   Part 1:     0.000041
#   Part 2:     1.446278
#  Elapsed:     1.44638


def parse(text):
    return [char == "1" for char in text]


def format(a):
    return "".join("1" if x else "0" for x in a)


def dragon(a, length):
    while len(a) < length:
        a = [*a, False, *(not x for x in reversed(a))]
    return a[:length]


def checksum(a):
    while len(a) % 2 == 0:
        a = [a[i] == a[i + 1] for i in range(0, len(a), 2)]
    return a


def part1(data, args, p1_state):
    return format(checksum(dragon(data, 272)))


def part2(data, args, p1_state):
    return format(checksum(dragon(data, 35651584)))


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
