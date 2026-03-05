def parse(text):
    return int(text)


def is_open(coord, fav):
    x, y = coord
    return (
        x >= 0
        and y >= 0
        and ((x * x + 3 * x + 2 * x * y + y + y * y + fav).bit_count() % 2) == 0
    )


def explore(end: tuple[int, int], fav: int):
    done = set()
    cubs = [(1, 1)]
    steps = -1
    while True:
        steps += 1
        nxt_cubs = []
        for cub in cubs:
            if cub == end:
                return steps
            x, y = cub
            for n in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
                if n not in done:
                    done.add(n)
                    nx, ny = n
                    if (
                        x >= 0
                        and y >= 0
                        and (
                            (
                                nx * nx + 3 * nx + 2 * nx * ny + ny + ny * ny + fav
                            ).bit_count()
                            % 2
                        )
                        == 0
                    ):
                        nxt_cubs.append(n)
        # input((cubs, nxt_cubs))
        cubs = nxt_cubs


def part1(fav, args, p1_state):
    coords = args[1:]
    if coords:
        start = tuple(map(int, coords))
    else:
        start = 31, 39
    return explore(start, fav)


def part2(fav, args, p1_state):
    return "ans2"


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
