#  Day 01
#  ======
#
#  Part 1: 246
#  Part 2: 124
#
#  Timings
#  ---------------------
#    Parse:     0.000022
#   Part 1:     0.000012
#   Part 2:     0.000071
#  Elapsed:     0.000148


DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
NORTH = 0


def parse(text):
    return [(1 if line[0] == "R" else -1, int(line[1:])) for line in text.split(", ")]


def part1(instructions, args, state_for_part2):
    print(len(instructions))
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
    for turn, count in instructions:
        dir = (dir + turn) % 4
        dx, dy = DIRS[dir]
        for _ in range(count):
            x += dx
            y += dy
            if (x, y) in visited:
                return abs(x) + abs(y)
            visited.add((x, y))


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
