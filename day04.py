
# intentionally overusing itertools :-)
from itertools import groupby

def parse(text):
    def parse_line(line):
        parts = line[:-7].split("-")
        return parts[:-1], int(parts[-1]), line[-6:-1]
    return [parse_line(line) for line in text.splitlines()]


def check_sum(name_parts):
    groups = [(key, list(grpr)) for key, grpr in groupby(sorted("".join(name_parts)))]
    return "". join(key for key, _ in sorted(groups, key=lambda grp: (-len(grp[1]), grp[0])))[:5]


def part1(data, args, state_for_part2):
    return sum(room[1] for room in data if check_sum(room[0])==room[2])


def part2(data, args, state_from_part1):
    return "ans2"


def jingle(filename=None, filepath=None, text=None, extra_args=None):
    import sack

    text = text if text else sack.read_input(filename, filepath)
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    extra_args = sys.argv[1:] if len(sys.argv) > 1 else []
    jingle(filename=filename, extra_args=extra_args)
