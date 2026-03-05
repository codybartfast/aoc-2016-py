#  Day 13
#  ======
#
#  Part 1: 96
#  Part 2: 141
#
#  Timings
#  ---------------------
#    Parse:     0.000001
#   Part 1:     0.000239
#   Part 2:     0.000098
#  Elapsed:     0.000378

def parse(text):
    return int(text)


def is_open(coord, fav):
    x, y = coord
    return (
        x >= 0
        and y >= 0
        and (x * x + 3 * x + 2 * x * y + y + y * y + fav).bit_count() % 2 == 0
    )


def explore(end, fav, max_steps=10**18):
    cubs = [(1, 1)]
    done = set(cubs)
    open_count = len(cubs)
    steps = 0
    while steps < max_steps:
        next_cubs = []
        for cub in cubs:
            if cub == end:
                return steps
            x, y = cub
            for n in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
                if n not in done:
                    done.add(n)
                    if is_open(n, fav):
                        next_cubs.append(n)
        open_count += len(next_cubs)
        cubs = next_cubs
        steps += 1
    return open_count


def part1(fav, args, p1_state):
    return explore((31, 39), fav)


def part2(fav, args, p1_state):
    return explore((31, 39), fav, 50)


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
