#  Day 02
#  ======
#
#  Part 1: 56855
#  Part 2: B3C27
#
#  Timings
#  ---------------------
#    Parse:     0.000003
#   Part 1:     0.000159
#   Part 2:     0.000212
#  Elapsed:     0.000416


SQUARE_PAD = ["123", "456", "789"]
DIAMOND_PAD = ["  1  ", " 234 ", "56789", " ABC ", "  D  "]


def parse(text):
    return text.splitlines()


def press_square(x, y, instrs):
    keys = []
    for seq in instrs:
        for dir in seq:
            match dir:
                case "U":
                    y = max(0, y - 1)
                case "R":
                    x = min(2, x + 1)
                case "D":
                    y = min(2, y + 1)
                case "L":
                    x = max(0, x - 1)
        keys.append(SQUARE_PAD[y][x])
    return keys


def press_diamond(x, y, instrs):
    keys = []
    for seq in instrs:
        for dir in seq:
            x2, y2 = x, y
            match dir:
                case "U":
                    y2 -= 1
                case "R":
                    x2 += 1
                case "D":
                    y2 += 1
                case "L":
                    x2 -= 1
            if abs(x2 - 2) + abs(y2 - 2) < 3:
                x, y = x2, y2
        keys.append(DIAMOND_PAD[y][x])
    return keys


def part1(instrs, args, state_for_part2):
    return "".join(press_square(1, 1, instrs))


def part2(instrs, args, state_from_part1):
    return "".join(press_diamond(0, 2, instrs))


def jingle(filename=None, filepath=None, text=None, extra_args=None):
    import sack

    text = text if text else sack.read_input(filename, filepath)
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    extra_args = sys.argv[1:] if len(sys.argv) > 2 else None
    jingle(filename=filename, extra_args=extra_args)
