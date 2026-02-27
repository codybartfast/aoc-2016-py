#  Day 09
#  ======
#
#  Part 1: 112830
#  Part 2: ans2
#
#  Timings
#  ---------------------
#    Parse:     0.000000
#   Part 1:     0.000013
#   Part 2:     0.000000
#  Elapsed:     0.000047

from day03 import count
def parse(text):
    return text


def calc_length(data):
    length = 0
    idx = 0
    while idx < len(data):
        if data[idx] != "(":
            # print(data[idx], end="")
            length += 1
            idx += 1
        else:
            count_digits = ""
            rep_digits = ""

            idx += 1
            while data[idx] != "x":
                count_digits += data[idx]
                idx += 1
            idx +=1
            while data[idx] != ")":
                rep_digits += data[idx]
                idx += 1
            idx += 1
            count = int(count_digits)
            # print(f"<span {count * int(rep_digits)}>", end="")
            length += count * int(rep_digits)
            idx += count
    # print("\n")
    return length
            
            

def part1(data, args, p1_state):
    return calc_length(data)


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
