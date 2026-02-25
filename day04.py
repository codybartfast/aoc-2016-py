from itertools import groupby

CHARS = "abcdefghijklmnopqrstuvwxyz"


def parse(text):
    def parse_line(line):
        return line[:-11], int(line[-10:-7]), line[-6:-1]

    return [parse_line(line) for line in text.splitlines()]


def checksum(name):
    groups = ((key, list(grpr)) for key, grpr in groupby(sorted(name)))
    return "".join(
        key
        for key, _ in sorted(groups, key=lambda grp: (-len(grp[1]), grp[0]))
        if key != "-"
    )[:5]


def part1(rooms, args, state_for_part2):
    return sum(room[1] for room in rooms if checksum(room[0]) == room[2])


def part2(rooms, args, state_from_part1):
    for room in rooms:
        encrpted, sector, csum = room
        if checksum(encrpted) == csum:
            shift = sector % 26
            trans = str.maketrans(CHARS, CHARS[shift:] + CHARS[:shift])
            name = encrpted.translate(trans)
            if "north" in name:
                return sector


def jingle(filename=None, filepath=None, text=None, extra_args=None):
    import sack

    text = text if text else sack.read_input(filename, filepath)
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    extra_args = sys.argv[1:] if len(sys.argv) > 1 else []
    jingle(filename=filename, extra_args=extra_args)
