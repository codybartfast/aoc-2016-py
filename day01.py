DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
NORTH = 0

def parse(text):
    def parse_line(line):
        return [parts for parts in line.split()]

    return [(1 if line[0] == "R" else -1, int(line[1:])) for line in text.split(", ")]


def part1(instructions, args, state_for_part2):
    print(instructions)
    dir = NORTH
    (x, y) = (0, 0)
    for turn, count in instructions:
        dir = (dir + turn) % 4
        dx, dy = DIRS[dir]
        x += dx * count
        y += dy * count

    return abs(x) + abs(y)


def part2(data, args, state_from_part1):
    return "ans2"


def jingle(filename=None, filepath=None, text=None, extra_args=None):
    import sack

    text = text if text else sack.read_input(filename, filepath)
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    extra_args = sys.argv[1:] if len(sys.argv) > 2 else None
    jingle(filename=filename, extra_args=extra_args)
