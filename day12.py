#  Day 12
#  ======
#
#  Part 1: 318007
#  Part 2: 9227661
#
#  Timings
#  ---------------------
#    Parse:     0.000019
#   Part 1:     0.072167
#   Part 2:     1.859008
#  Elapsed:     1.931301

def parse(text):
    instrs = ["cpy", "inc", "dec", "jnz"]
    regs = ["pc", "a", "b", "c", "d"]

    def convert(val):
        if val in regs:
            return (1, regs.index(val))
        return (0, int(val))

    def parse_line(line):
        parts = line.split()
        return instrs.index(parts[0]), tuple(map(convert, parts[1:]))

    return [parse_line(line) for line in text.splitlines()]


def run(prog, regs):
    while regs[0] < len(prog):
        instr, args = prog[regs[0]]
        match instr:
            case 0:
                arg0, arg1 = args
                regs[arg1[1]] = arg0[1] if not arg0[0] else regs[arg0[1]]
                regs[0] += 1
            case 1:
                regs[args[0][1]] += 1
                regs[0] += 1
            case 2:
                regs[args[0][1]] -= 1
                regs[0] += 1
            case 3:
                arg0, arg1 = args
                regs[0] += (
                    (arg1[1] if not arg1[0] else regs[arg1[1]])
                    if (arg0[1] if not arg0[0] else regs[arg0[1]])
                    else 1
                )
    return regs


def part1(program, args, p1_state):
    return run(program, [0, 0, 0, 0, 0])[1]


def part2(program, args, p1_state):
    return run(program, [0, 0, 0, 1, 0])[1]


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
