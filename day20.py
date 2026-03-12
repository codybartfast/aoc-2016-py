def parse(text):
    def parse_line(line):
        parts = line.split("-")
        return int(parts[0]), int(parts[1])

    return [parse_line(line) for line in text.splitlines()]


def part1(excluded, args, p1_state):
    excluded.sort()

    allowed = [(0, 2**32 - 1)]

    alw_idx = 0
    alw_start, alw_end = allowed[alw_idx]

    exl_idx = 0
    exl_start, exl_end = excluded[exl_idx]

    while alw_idx < len(allowed) and exl_idx < len(excluded):
        alw_start, alw_end = allowed[alw_idx]
        exl_start, exl_end = excluded[exl_idx]

        if alw_end < exl_start:
            alw_idx += 1
        elif alw_start <= exl_end:
            allowed.pop(alw_idx)
            if alw_start < exl_start:
                allowed.insert(alw_idx, (alw_start, exl_start - 1))
                alw_idx += 1
            if exl_end < alw_end:
                allowed.insert(alw_idx, (exl_end + 1, alw_end))
            exl_idx += 1
        else:
            exl_idx += 1

    return allowed[0][0]


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
        extra_args = sys.argv[2:] if len(sys.argv) > 2 else []
        jingle(filepath=filepath, extra_args=extra_args)
