def parse(text):
    def convert(val):
        if val in ["a", "b", "c", "d"]:
            return (1, ord(val) - 96)
        return (0, int(val))

    def parse_line(line):
        parts = line.split()
        return parts[0], tuple(map(convert, parts[1:]))

    return [parse_line(line) for line in text.splitlines()]


def run(prog, regs):
    while regs[0] < len(prog):
        instr, args = prog[regs[0]]
        match instr, args:
            case "cpy", ((t1, v1), (_, v2)):
                regs[v2] = v1 if not t1 else regs[v1]
                regs[0] += 1
            case "inc", ((_, v1),):
                regs[v1] += 1
                regs[0] += 1
            case "dec", ((_, v1),):
                regs[v1] -= 1
                regs[0] += 1
            case "jnz", ((t1, v1), (t2, v2)):
                regs[0] += (
                    (v2 if not t2 else regs[v2]) if (v1 if not t1 else regs[v1]) else 1
                )
            case _:
                assert False, (instr, args)
    return regs


def part1(data, args, p1_state):
    return run(data, [0] * 5)[1]


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
