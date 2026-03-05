from hashlib import md5
import re


def parse(text):
    return text.encode()


def digests(prefix):
    index = -1
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
        index += 1
        yield (index, hash.hexdigest())


def otps(salt):
    trip_re = re.compile(r"(.)\1\1")
    quint_re = re.compile(r"(.)\1\1\1\1")

    candidates = {}
    for index, digest in digests(salt):
        if m := quint_re.search(digest):
            val = m.group(1)
            cands = candidates[val]
            lim = index - 1000
            for cand in cands:
                if cand >= lim:
                    yield cand
            cands.clear()

        if m := trip_re.search(digest):
            candidates.setdefault(m.group(1), []).append(index)


def part1(salt, args, p1_state):
    otp_iter = otps(salt)
    indexes = sorted([next(otp_iter) for _ in range(64)])
    safe_limit = indexes[-1] + 1000
    while (index := next(otp_iter)) <= safe_limit:
        indexes.append(index)
    # print(len(indexes))
    # print(sorted(indexes)[:64])
    return sorted(indexes)[63]


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
