#  Day 01
#  ======
#
#  Part 1: 246
#  Part 2: 124
#
#  Timings
#  ---------------------
#    Parse:     0.000018
#   Part 1:     0.000011
#   Part 2:     0.000121
#  Elapsed:     0.000192

DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
NORTH = 0


def parse(text):
    def parse_line(line):
        return [parts for parts in line.split()]

    return [(1 if line[0] == "R" else -1, int(line[1:])) for line in text.split(", ")]


def part1(instructions, args, state_for_part2):
    dir = NORTH
    (x, y) = (0, 0)
    for turn, count in instructions:
        dir = (dir + turn) % 4
        dx, dy = DIRS[dir]
        x += dx * count
        y += dy * count

    return abs(x) + abs(y)


def part2(instructions, args, state_from_part1):
    dir = NORTH
    (x, y) = (0, 0)
    visited = set([(x, y)])
    revisited = None
    for turn, count in instructions:
        dir = (dir + turn) % 4
        dx, dy = DIRS[dir]
        for _ in range(count):
            x += dx
            y += dy
            if (x, y) in visited and not revisited:
                revisited = (x, y)
            else:
                visited.add((x, y))

    if revisited:
        return abs(revisited[0]) + abs(revisited[1])


def jingle(filename=None, filepath=None, text=None, extra_args=None):
    import sack

    text = text if text else sack.read_input(filename, filepath)
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    extra_args = sys.argv[1:] if len(sys.argv) > 2 else None
    jingle(filename=filename, extra_args=extra_args)
