def parse(text):
    return text.splitlines()


def does_support_tls(address):
    len = 0
    depth = 0
    got_abba = False
    for idx, char in enumerate(address):
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
                        address[idx - 3] == char
                        and address[idx - 2] == address[idx - 1]
                        and address[idx - 1] != char
                    ):
                        if depth == 0:
                            got_abba = True
                        else:
                            return False
    return got_abba


def does_support_ssl(address):
    len = 0
    depth = 0
    super_trips = set()
    hyper_trips = set()
    for idx, char in enumerate(address):
        match char:
            case "[":
                len = 0
                depth += 1
            case "]":
                len = 0
                depth -= 1
            case _:
                len += 1
                if len >= 3:
                    prev = address[idx - 1]
                    if address[idx - 2] == char and prev != char:
                        if depth:
                            this, other = hyper_trips, super_trips
                        else:
                            this, other = super_trips, hyper_trips
                        twin = prev + char + prev
                        if twin in other:
                            return True
                        this.add(char + prev + char)
    return False


def part1(data, args, p1_state):
    return sum(1 for address in data if does_support_tls(address))


def part2(data, args, p1_state):
    return sum(1 for address in data if does_support_ssl(address))


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
