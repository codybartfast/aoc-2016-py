def parse(text):
    def parse_line(line):
        parts = line.split()
        return (int(parts[3]), int(parts[-1][:-1]))

    return [parse_line(line) for line in text.splitlines()]

def find_start(discs):
    time = 0
    period = 1
    for size, slot in discs:
        time += 1
        slot = (slot + time) % size
        while slot:
            time += period
            slot = (slot + period) % size
        period *= size
    return time - len(discs)
        

def part1(discs, args, p1_state):
    print(f"{discs}\n\n")
    return find_start(discs)


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
