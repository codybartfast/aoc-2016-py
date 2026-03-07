from itertools import islice


def parse(text):
    a = 0
    for char in text:
        a <<= 1
        if char == "1":
            a |= 1
    return a, len(text)


def dragon(a, n_a, n_target):
    while n_a < n_target:
        t = a
        a <<= 1
        for _ in range(n_a):
            a <<= 1
            a |= not (t & 1)
            t >>= 1
        n_a = n_a * 2 + 1
    a >>= n_a - n_target
    return a


def checksum(a, n_a):
    def round(a, n):
        chk = 0
        while n:
            chk <<= 1
            chk |= 1 if (a & 0b11 == 0b11 or a & 0b11 == 0b00) else 0
            a >>= 2
            n -= 1
        return chk

    is_reversed = False
    while n_a % 2 == 0:
        is_reversed = not is_reversed
        n_a //= 2
        a = round(a, n_a)

    if is_reversed:
        t = a
        a = 0
        for _ in range(n_a):
            a <<= 1
            a |= t & 1
            t >>= 1
    return f"{a:0{n_a}b}"


def part1(data, args, p1_state):
    a, n_a = data
    expanded = 272
    return checksum(dragon(a, n_a, expanded), expanded)


def part2(data, args, p1_state):
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
