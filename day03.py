import itertools


def parse(text):
    return [tuple(map(int, line.split())) for line in text.splitlines()]


def part1(triangles, args, state_for_part2):
    return sum(1 for (a, b, c) in map(sorted, triangles) if a + b > c)


def part2(triangles, args, state_from_part1):
    triangles = itertools.chain.from_iterable(
        map(lambda batch: zip(*batch), itertools.batched(triangles, 3))
    )
    return sum(1 for (a, b, c) in map(sorted, triangles) if a + b > c)


def jingle(filename=None, filepath=None, text=None, extra_args=None):
    import sack

    text = text if text else sack.read_input(filename, filepath)
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    extra_args = sys.argv[1:] if len(sys.argv) > 2 else None
    jingle(filename=filename, extra_args=extra_args)
