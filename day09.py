#  Day 09
#  ======
#
#  Part 1: 112830
#  Part 2: 10931789799
#
#  Timings
#  ---------------------
#    Parse:     0.000000
#   Part 1:     0.000013
#   Part 2:     0.000751
#  Elapsed:     0.000806


def parse(text):
    return text


def decomp_length(data, start=None, end=None, ver="v2"):
    idx = start if start else 0
    end = end if end else len(data)
    dc_len = 0
    while idx < end:
        if data[idx] != "(":
            dc_len += 1
            idx += 1
        else:
            cmpr_len_digits = ""
            rept_digits = ""

            idx += 1
            while data[idx] != "x":
                cmpr_len_digits += data[idx]
                idx += 1
            idx += 1
            while data[idx] != ")":
                rept_digits += data[idx]
                idx += 1
            idx += 1
            cmpr_len = int(cmpr_len_digits)
            dc_len += int(rept_digits) * (
                decomp_length(data, idx, idx + cmpr_len) if ver == "v2" else cmpr_len
            )
            idx += cmpr_len
    return dc_len


def part1(data, args, p1_state):
    return decomp_length(data, ver="v1")


def part2(data, args, p1_state):
    return decomp_length(data, ver="v2")


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
