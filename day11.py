import re


class Facility:
    def __init__(self, floors):
        self.floors = floors
        self.size = len(floors)
        self.flr = self.size - 1
        self.count = 0
        self.have_collected_gens = False

    def gens(self, flr=None):
        if flr is None:
            flr = self.flr
        return self.floors[flr][0]

    def chips(self, flr=None):
        if flr is None:
            flr = self.flr
        return self.floors[flr][1]

    def find_gen(self, gen):
        for flr in range(self.size):
            if gen in self.gens(flr):
                return flr

    def find_chip(self, chip):
        for flr in range(self.size):
            if chip in self.chips(flr):
                return flr


def parse(text):
    rx = re.compile(r"(\w+)(?:-\w+)? (generator|microchip)")

    def parse_line(line):
        floor = [[], []]
        for material, type in rx.findall(line):
            floor[0 if type == "generator" else 1].append(material[:2].title())
        return floor

    floors = [parse_line(line) for line in reversed(text.splitlines())]
    return Facility(floors)


# reversed floors

# Strategy?
#   - if at top:
#     - done?
#     - move a chip down
#   - try:
#     - move a pair up
#     - ? move a gen up
#     - pair a chip
#       - up (but not top)
#       - down
#     - move so can pair


def display(facility: Facility):
    print()
    print(facility.flr)
    for i, floor in enumerate(facility.floors):
        print("E" if i == facility.flr else " ", floor)
        # print(floor)
    print("count:", facility.count)


def is_valid(facility: Facility):
    for floor in facility.floors:
        if floor[1] and floor[0] and any(kind not in floor[0] for kind in floor[1]):
            assert False  # Invalid State
    return True


def done(facility: Facility):
    return not any(lst for floor in facility.floors for lst in floor)


def is_vulnerable(floor):
    gens, chips = floor
    return any(chip for chip in chips if chip not in gens)


def is_safe(facility, flr, chip):
    if 0 <= flr < facility.size:
        gens = facility.gens(flr)
        return not gens or chip in gens


def unit(n):
    return n // abs(n)


def next_floor(facility, dest):
    return facility.flr + unit(dest - facility.flr)


def move_pair_up(facility: Facility):
    floors, flr = facility.floors, facility.flr
    upper = floors[flr - 1]
    if is_vulnerable(upper):
        # print("m is vulnerable")
        return None
    gens, chips = floors[flr]
    pairs = [el for el in gens if el in chips]
    if not pairs:
        # print("m no pairs")
        return None

    print("m start")
    pair = pairs[0]
    dest = facility.flr - 1
    # print("Flr:", facility.flr, "Dest:", dest, "Pair:", pair)
    facility.chips().remove(pair)
    facility.gens().remove(pair)
    # display(facility)
    facility.chips(dest).append(pair)
    facility.gens(dest).append(pair)
    # display(facility)
    facility.flr = dest
    facility.count += 1
    # print("m done")
    return facility


def drop_something(facility):
    flr = 1
    while not facility.gens(flr) and not facility.chips(flr):
        flr += 1
    if facility.gens(flr):
        facility.gens(flr).append(facility.gens().pop())
    else:
        facility.chips(flr).append(facility.chips().pop())
    facility.count += flr
    facility.flr = flr
    return facility


def reunite_chip(facility):
    unmatched = [chip for chip in facility.chips() if chip not in facility.gens()]
    if not unmatched:
        return None

    print("ru start")
    opts = [(chip, next_floor(facility, facility.find_gen(chip))) for chip in unmatched]
    if len(set(opt[1] for opt in opts)) != 1:
        assert False  # need to make choices
    for opt in opts[:2]:
        chip, dest = opt
        facility.chips().remove(chip)
        facility.chips(dest).append(chip)
    facility.flr = opts[0][1]
    facility.count += 1
    return facility


def reposition(facility):
    print("rp start")
    unmatched = []
    for flr in range(facility.size):
        for unm in (
            chip for chip in facility.chips(flr) if chip not in facility.gens(flr)
        ):
            unmatched.append(flr)
    assert unmatched
    unmatched.sort(key=lambda unm_flr: abs(unm_flr - facility.flr))
    new_flr = unmatched[0]
    if abs(new_flr - facility.flr) > 1:
        assert False  # think 1) safe 2) loops 3) correct count
    facility.chips(new_flr).append(facility.chips().pop())
    facility.flr = new_flr
    facility.count += 1
    return facility


def move_things(facility):
    while not done(facility):
        display(facility)
        is_valid(facility)
        input("...")
        if facility.flr == 0:
            drop_something(facility)
        else:
            rslt = move_pair_up(facility)
            if not rslt:
                rslt = reunite_chip(facility)
            if not rslt:
                rslt = reposition(facility)

    print("\nDone")
    display(facility)


def part1(facility, args, p1_state):
    move_things(facility)
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
