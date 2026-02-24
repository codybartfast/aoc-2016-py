def parse(text):
    def parse_line(line):
        return [parts for parts in line.split()]

    return [parse_line(line) for line in text.splitlines()]


def part1(data, args, state_for_part2):
    print(f"{data}\n\n")
    return "ans1"


def part2(data, args, state_from_part1):
    return "ans2"


def jingle(filename=None, filepath=None, text=None, extra_args=None):
    import sack

    text = text if text else sack.read_input(filename, filepath)
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    extra_args = sys.argv[1:] if len(sys.argv) > 2 else None
    jingle(filename=filename, extra_args=extra_args)
