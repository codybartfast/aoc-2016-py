#  Day 14
#  ======
#
#  Part 1: 25427
#  Part 2: 22045
#
#  Timings
#  ---------------------
#    Parse:     0.000001
#   Part 1:     0.024795
#   Part 2:    12.927354
#  Elapsed:    12.952210

from hashlib import md5
import re


def parse(text):
    return text.encode()


def digests(prefix, stretch):
    index = 0
    prefix_hash = md5(prefix)
    bs = bytearray([0x2F])
    last_idx = 0
    idx = last_idx
    while True:
        if bs[idx] < 0x39:
            bs[idx] += 1
            idx = last_idx
        else:
            bs[idx] = 0x30
            if idx > 0:
                idx -= 1
                continue
            else:
                bs.insert(0, 0x31)
                last_idx += 1
                idx = last_idx
        hash = prefix_hash.copy()
        hash.update(bs)
        if stretch:
            for _ in range(2016):
                hash = md5(hash.hexdigest().encode())
        yield (index, hash.hexdigest())
        index += 1


def otps(salt, stretch):
    trip_re = re.compile(r"(.)\1\1")
    quint_re = re.compile(r"(.)\1\1\1\1")

    candidates = {}
    for index, digest in digests(salt, stretch):
        if m := quint_re.search(digest):
            cands = candidates[m.group(1)]
            lim = index - 1000
            for cand in cands:
                if cand >= lim:
                    yield cand
            cands.clear()

        if m := trip_re.search(digest):
            candidates.setdefault(m.group(1), []).append(index)


def find_index(salt, key_num, stretch = False):
    otp_iter = otps(salt, stretch)
    indexes = sorted([next(otp_iter) for _ in range(key_num)])
    safe_limit = indexes[-1] + 1000
    while (index := next(otp_iter)) <= safe_limit:
        indexes.append(index)
    return sorted(indexes)[key_num - 1]


def part1(salt, args, p1_state):
    return find_index(salt, 64)


def part2(salt, args, p1_state):
    return find_index(salt, 64, True)


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
