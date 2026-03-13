#  2016 Day 21
#  ===========
#
#  Part 1: gbhcefad
#  Part 2: gahedfcb
#
#  Timings
#  ---------------------
#    Parse:     0.000052
#   Part 1:     0.000035
#   Part 2:     0.000036
#  Elapsed:     0.000167


def parse(text):
    def parse_line(line):
        parts = line.split()
        match parts:
            case ["swap", "position", x, "with", "position", y]:
                return ("swap_pstn", int(x), int(y))
            case ["swap", "letter", x, "with", "letter", y]:
                return ("swap_ltr", x, y)
            case ["rotate", "left", x, _]:
                return ("rotate", int(x))
            case ["rotate", "right", x, _]:
                return ("rotate", -int(x))
            case ["rotate", "based", "on", "position", "of", "letter", x]:
                return ("rot_on_ltr_pstn", x)
            case ["reverse", "positions", x, "through", y]:
                return ("reverse", int(x), int(y))
            case ["move", "position", x, "to", "position", y]:
                return ("move", int(x), int(y))
            case _:
                assert False, parts

    return [parse_line(line) for line in text.splitlines()]


def apply(operations, word):
    for op in operations:
        match op:
            case "swap_pstn", x, y:
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "swap_ltr", a, b:
                x = word.index(a)
                y = word.index(b)
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "rotate", n:
                word = word[n:] + word[:n]
            case "rot_on_ltr_pstn", a:
                x = word.index(a)
                n = -((1 + x + (x >= 4)) % len(word))
                word = word[n:] + word[:n]
            case "reverse", x, y:
                assert x < y
                word[x : y + 1] = word[x : y + 1][::-1]
            case "move", x, y:
                a = word.pop(x)
                word.insert(y, a)
            case _:
                assert False, op
    return word


def unapply(operations, word):
    based_on_destinations = [
        ((1 + x + x + (x >= 4)) % len(word)) for x in range(len(word))
    ]
    assert len(based_on_destinations) == len(set(based_on_destinations))
    while operations:
        op = operations.pop()
        match op:
            case "swap_pstn", x, y:
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "swap_ltr", a, b:
                x = word.index(a)
                y = word.index(b)
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "rotate", n:
                n = -n  #
                word = word[n:] + word[:n]
            case "rot_on_ltr_pstn", a:
                x = word.index(a)
                orig_x = based_on_destinations.index(x)
                n = (x - orig_x) % len(word)
                word = word[n:] + word[:n]
            case "reverse", x, y:
                x, y = (x, y) if x < y else (y, x)  #
                word[x : y + 1] = word[x : y + 1][::-1]
            case "move", x, y:
                a = word.pop(y)
                word.insert(x, a)
            case _:
                assert False, op
    return word


def part1(operations, args, p1_state):
    return "".join(apply(operations, list("abcdefgh")))


def part2(operations, args, p1_state):
    return "".join(unapply(operations, list("fbgdceah")))


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
        extra_args = sys.argv[2:] if len(sys.argv) > 2 else []
        jingle(filepath=filepath, extra_args=extra_args)
