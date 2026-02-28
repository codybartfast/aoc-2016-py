import re

CHIPS = 0
GENS = 1


def parse(text):
    rx = re.compile(r"(\w+)(?:-\w+)? (generator|microchip)")

    def parse_line(line):
        floor = [[], []]
        for material, type in rx.findall(line):
            floor[GENS if type == "generator" else CHIPS].append(material[:2].title())
        return floor

    return [parse_line(line) for line in text.splitlines()]


# Strategy?
#   - try move a generator up
#   - if can't, move a microchip down
#   - if all gens up - tidy chips
#   - probably don't want to go up with just 1 item.


def display(floors):
    for floor in reversed(floors):
        print(floor)


def is_valid(floors):
    for floor in floors:
        if (
            floor[CHIPS]
            and floor[GENS]
            and any(kind not in floor[GENS] for kind in floor[CHIPS])
        ):
            return False
    return True


def part1(floors, args, p1_state):
    display(floors)
    print(is_valid(floors))
    floors[0][CHIPS].remove("Pr")
    floors[1][CHIPS].append("Pr")
    display(floors)
    print(is_valid(floors))
    return "ans1"


def part2(floors, args, p1_state):
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
