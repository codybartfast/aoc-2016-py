from itertools import islice

PC = 0
REG_A = 1


def parse(text):
    regs = ["pc", "a", "b", "c", "d"]

    def convert(val):
        if val in regs:
            return (1, regs.index(val))
        return (0, int(val))

    def parse_line(line):
        parts = line.split()
        return parts[0], tuple(map(convert, parts[1:]))

    return [parse_line(line) for line in text.splitlines()]


def run(prog, regs):
    while regs[0] < len(prog):
        instr, args = prog[regs[0]]
        match instr:
            case "cpy":
                (arg0_type, arg0_val), (arg1_type, arg1_val) = args
                if arg1_type:
                    regs[arg1_val] = regs[arg0_val] if arg0_type else arg0_val
                regs[PC] += 1
            case "inc":
                [(type, val)] = args
                if type:
                    regs[val] += 1
                regs[PC] += 1
            case "dec":
                [(type, val)] = args
                if type:
                    regs[val] -= 1
                regs[PC] += 1
            case "jnz":
                (arg0_type, arg0_val), (arg1_type, arg1_val) = args
                regs[PC] += (
                    (regs[arg1_val] if arg1_type else arg1_val)
                    if (regs[arg0_val] if arg0_type else arg0_val)
                    else 1
                )
            case "out":
                [(type, val)] = args
                yield regs[val] if type else val
                regs[PC] += 1
            case _:
                assert False, instr
    return regs


def boot(a=0):
    regs = [0] * 5
    regs[REG_A] = a
    return regs


def part1(prog, args, p1_state):
    a = -1
    signal = ""
    target = "0101010101"
    while signal != target:
        a += 1
        signal = "".join(islice(map(str, run(prog, boot(a))), len(target)))
    return a


def part2(prog, args, p1_state):
    return "Merry Christmas!"


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
        extra_args = sys.argv[2:] if len(sys.argv) > 2 else []
        jingle(filepath=filepath, extra_args=extra_args)
