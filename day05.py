#  Day 05
#  ======
#
#  Part 1: 801b56a7
#  Part 2: 424a0197
#
#  Timings
#  ---------------------
#    Parse:     0.000001
#   Part 1:     2.113934
#   Part 2:     4.780004
#  Elapsed:     6.894021

# I wonderd if the real perf hit with this was the construction of the candidates
# like ("abc" + str(i)).encode() rather than the hashing. So I did some bit twiddling
# and it looks like this is an order of magnitude faster than many solutions.

from hashlib import md5


def parse(text):
    return text.encode()


def hash_search(prefix):
    pfx_hash = md5(prefix)
    suffix = bytearray([0x2F]) # char before '0'
    last_idx = 0
    idx = last_idx
    while True:
        if suffix[idx] != 0x39: # '9'
            suffix[idx] += 1
            idx = last_idx
        else:
            suffix[idx] = 0x30 # '0'
            if idx > 0:
                idx -= 1
                continue
            else:
                suffix.insert(0, 0x31) # '1'
                last_idx += 1
                idx = last_idx
        hash = pfx_hash.copy()
        hash.update(suffix)
        if (
            not hash.digest()[0]
            and not hash.digest()[1]
            and not hash.digest()[2] & 0xF0
        ):
            yield hash.hexdigest()[5:7]


def find_passwords(pairs):
    pwd1 = ""
    pwd2 = [None] * 8
    for c1, c2 in pairs:
        if len(pwd1) < 8:
            pwd1 += c1
            if len(pwd1) == 8:
                yield pwd1
        if c1 in "01234567":
            pos = int(c1)
            if not pwd2[pos]:
                pwd2[pos] = c2
            if all(pwd2):
                yield "".join(pwd2)
                return


def part1(door_id, args, state_for_part2):
    passwords = find_passwords(hash_search(door_id))
    state_for_part2["passwords"] = passwords
    return next(passwords)


def part2(door_id, args, state_from_part1):
    return next(state_from_part1["passwords"])


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
