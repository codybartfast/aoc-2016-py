#  Day 06
#  ======
#
#  Part 1: qoclwvah
#  Part 2: ryrgviuv
#
#  Timings
#  ---------------------
#    Parse:     0.000016
#   Part 1:     0.000125
#   Part 2:     0.000002
#  Elapsed:     0.000181

from collections import Counter


def parse(text):
    return text.splitlines()


def part1(repitions, args, p1_state):
    most_commons = [Counter(col).most_common() for col in zip(*repitions)]
    p1_state.value = most_commons
    return "".join(mc[0][0] for mc in most_commons)


def part2(repitions, args, p1_state):
    return "".join(mc[-1][0] for mc in p1_state.value)


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
