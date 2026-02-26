def parse(text):
    return text.splitlines()


def does_support_tls(address):
    len = 0
    depth = 0
    got_abba = False
    for idx, char in enumerate(address):
        assert depth >= 0
        match char:
            case "[":
                depth += 1
                len = 0
            case "]":
                depth -= 1
                len = 0
            case _:
                len += 1
                if len >= 4:
                    if (
                        char == address[idx - 3]
                        and address[idx - 2] == address[idx - 1]
                        and address[idx - 1] != char
                    ):
                        if depth == 0:
                            got_abba = True
                        else:
                            return False
    return got_abba


def part1(data, args, p1_state):
    return sum(1 for address in data if does_support_tls(address))


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
