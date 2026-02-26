#  Day 03
#  ======
#
#  Part 1: 993
#  Part 2: 1849
#
#  Timings
#  ---------------------
#    Parse:     0.000924
#   Part 1:     0.000232
#   Part 2:     0.000368
#  Elapsed:     0.001567

import itertools


def parse(text):
    return [tuple(map(int, line.split())) for line in text.splitlines()]


def count(triangles):
    return sum(1 for (a, b, c) in map(sorted, triangles) if a + b > c)


def part1(triangles, args, state_for_part2):
    return count(triangles)


def part2(triangles, args, state_from_part1):
    return count(
        itertools.chain.from_iterable(
            map(lambda batch: zip(*batch), itertools.batched(triangles, 3))
        )
    )


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
