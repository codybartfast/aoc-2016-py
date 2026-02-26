#  Day 08
#  ======
#
#  Part 1: 106
#  Part 2: CFLELOYFCS
#
#  Timings
#  ---------------------
#    Parse:     0.000177
#   Part 1:     0.000078
#   Part 2:     0.000048
#  Elapsed:     0.000346

import re


def parse(text):
    rx = re.compile(r"(?:\w+ )?(\w+)?\D+(\d+)\D+(\d+)")

    def parse_line(line):
        (transf, n1, n2) = rx.match(line).groups()
        return transf, int(n1), int(n2)

    return [parse_line(line) for line in text.splitlines()]


def modify(screen, instr):
    transf, n1, n2 = instr
    match transf:
        case "rect":
            for x in range(n1):
                for y in range(n2):
                    screen[y][x] = "#"
        case "row":
            screen[n1] = screen[n1][-n2:] + screen[n1][:-n2]
        case "column":
            col = [screen[y][n1] for y in range(len(screen))]
            col = col[-n2:] + col[:-n2]
            for y in range(len(screen)):
                screen[y][n1] = col[y]


def part1(instructions, args, p1_state):
    w, h = 50, 6
    screen = [["."] * w for _ in range(h)]

    for instr in instructions:
        modify(screen, instr)

    p1_state.value = screen
    return sum(1 for row in screen for pixel in row if pixel == "#")


def part2(instructions, args, p1_state):
    import sack

    return sack.read_glyphs(p1_state.value)


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
