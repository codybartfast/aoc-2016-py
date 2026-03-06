#  Day 15
#  ======
#
#  Part 1: 122318
#  Part 2: 3208583
#
#  Timings
#  ---------------------
#    Parse:     0.000008
#   Part 1:     0.000006
#   Part 2:     0.000003
#  Elapsed:     0.000053


def parse(text):
    return [
        (int(parts[3]), int(parts[-1][:-1]))
        for parts in [line.split() for line in text.splitlines()]
    ]


def find_start(discs):
    time = 0
    period = 1
    for size, slot in discs:
        time += 1
        slot = (slot + time) % size
        while slot:
            time += period
            slot = (slot + period) % size
        period *= size
    return time - len(discs)


def part1(discs, args, p1_state):
    return find_start(discs)


def part2(discs, args, p1_state):
    discs.append((11, 0))
    return find_start(discs)


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
