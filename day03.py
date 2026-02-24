def parse(text):
    return [tuple(sorted(map(int, line.split()))) for line in text.splitlines()]


def part1(triangles, args, state_for_part2):
    # print(f"{triangles}\n\n")
    return sum(1 for (a, b, c) in triangles if a + b > c)


def part2(triangles, args, state_from_part1):
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
