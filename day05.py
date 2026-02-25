#  ======
#
#  Part 1: 801b56a7
#  Part 2: 424a0197
#
#  Timings
#  ---------------------
#    Parse:     0.000001
#   Part 1:     2.206225
#   Part 2:     7.230639
#  Elapsed:     9.436959


from hashlib import md5
from itertools import islice


def parse(text):
    return text.encode()


def search(prefix):
    target = "0" * 5
    base = md5(prefix)
    sfx = bytearray([0x2F])
    last_idx = 0
    idx = last_idx
    while True:
        if sfx[idx] == 0x39:
            sfx[idx] = 0x30
            if idx == 0:
                sfx.insert(0, 0x31)
                last_idx += 1
                idx = last_idx
            else:
                idx -= 1
                continue
        else:
            sfx[idx] += 1
            idx = last_idx
        hash = base.copy()
        hash.update(sfx)
        if hash.hexdigest().startswith(target):
            yield hash.hexdigest()[5:7]


def part1(data, args, state_for_part2):
    return "".join(pair[0] for pair in islice(search(data), 8))


def part2(data, args, state_from_part1):
    pwd = ["-"] * 8
    for pair in search(data):
        pos, val = pair[0], pair[1]
        if pos in "01234567":
            pos = int(pos)
            if pwd[pos] == "-":
                pwd[pos] = val
            if "-" not in pwd:
                break
        else:
            continue
    return "".join(pwd)


def jingle(filename=None, filepath=None, text=None, extra_args=None):
    import sack

    text = text if text else sack.read_input(filename, filepath)
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    extra_args = sys.argv[1:] if len(sys.argv) > 1 else []
    jingle(filename=filename, extra_args=extra_args)
