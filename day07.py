#  Day 07
#  ======
#
#  Part 1: 115
#  Part 2: 231
#
#  Timings
#  ---------------------
#    Parse:     0.000172
#   Part 1:     0.005389
#   Part 2:     0.009124
#  Elapsed:     0.014730
#
# Regex is a touch faster for Part 1 but a lot slower for Part 2, I redid with
# regex because I'm a bit rusty with them, so there may be other much faster
# regex solutions

import re


def parse(text):
    return text.splitlines()


def does_support_ssl(address):
    len = 0
    depth = 0
    super_trips = set()
    hyper_trips = set()
    for idx, char in enumerate(address):
        match char:
            case "[":
                len = 0
                depth += 1
            case "]":
                len = 0
                depth -= 1
            case _:
                len += 1
                if len >= 3:
                    prev = address[idx - 1]
                    if address[idx - 2] == char and prev != char:
                        if depth:
                            this, other = hyper_trips, super_trips
                        else:
                            this, other = super_trips, hyper_trips
                        if prev + char + prev in other:
                            return True
                        this.add(char + prev + char)
    return False


def part1(addresses, args, p1_state):
    super_abba = re.compile(r"(\w)(?!\1)(\w)\2\1(?!\w*\])")
    hyper_abba = re.compile(r"(\w)(?!\1)(\w)\2\1(?=\w*\])")
    return sum(
        1
        for addr in addresses
        if super_abba.search(addr) and not hyper_abba.search(addr)
    )


def part2(addresses, args, p1_state):
    return sum(1 for addr in addresses if does_support_ssl(addr))

    # aba = re.compile(r"(?=.*?(\w)(?!\1)(\w)\1(?!\w*\]))(?=.*?\2\1\2(?=\w*\]))")
    # bab = re.compile(r"(?=.*?(\w)(?!\1)(\w)\1(?=\w*\]))(?=.*?\2\1\2(?!\w*\]))")
    # return sum(1 for addr in addresses if aba.search(addr) or bab.search(addr))


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
