def parse(text):
    return [False, *[char == "^" for char in text], False]


def format(row):
    return "".join("^" if b else "." for b in row[0:])


def next(row):
    return [False, *[row[i - 1] ^ row[i + 1] for i in range(1, len(row) - 1)], False]


def part1(row, args, p1_state):
    total = 0
    for _ in range(40):
        total += len(row) - sum(row) - 2
        row = next(row)
    return total


def part2(row, args, p1_state):
    total = 0
    for _ in range(400_000):
        # print(format(row))
        total += len(row) - sum(row) - 2
        row = next(row)
    return total


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
