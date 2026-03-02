import re

UP = +1
DOWN = -1


def parse(text):
    rx = re.compile(r"(\w+)(?:-\w+)? (generator|microchip)")

    def parse_line(line):
        floor = [[], []]
        for material, type in rx.findall(line):
            floor[0 if type == "generator" else 1].append(material[:2].title())
        return floor

    floors = [parse_line(line) for line in (text.splitlines())]
    return Facility(floors)


# reversed floors

# Strategy #3?
#   - clear all from 1st except one chip
#   - move chips down from 3rd except one chip
#   - move up first pair
#   - jiggle up remaining pairs on 2nd, but one
#   - move up last 2nd pair
#   - move up 1st chip


class Facility:
    def __init__(self, floors):
        self.floors = floors
        self.size = len(floors)
        self.flr = 0
        self.count = 0
        self.have_collected_gens = False

    def display(self):
        lines = [f"{"E" if i == self.flr else " "} {floor}" for i, floor in enumerate(self.floors)]
        print("\n".join(reversed(lines)))
        print("count:", self.count)
        print()

    def done(self):
        return not any(lst for floor in self.floors for lst in floor)

    def gens(self, flr=None):
        if flr is None:
            flr = self.flr
        return self.floors[flr][0]

    def chips(self, flr=None):
        if flr is None:
            flr = self.flr
        return self.floors[flr][1]

    def is_valid(self):
        for floor in self.floors:
            if floor[1] and floor[0] and any(kind not in floor[0] for kind in floor[1]):
                assert False  # Invalid State
        return True

    def find_gen(self, gen):
        for flr in range(self.size):
            if gen in self.gens(flr):
                return flr

    def find_chip(self, chip):
        for flr in range(self.size):
            if chip in self.chips(flr):
                return flr

    def by_matched(self, flr=None):
        if flr is None:
            flr = self.flr
        gens, chips = self.gens(flr), self.chips(flr)
        # print(self.flr, self.floors[self.flr], gens, chips)
        pairs = [el for el in gens if el in chips]
        lone_gens = [el for el in gens if el not in pairs]
        lone_chips = [el for el in chips if el not in pairs]
        return lone_gens, pairs, lone_chips

    def move(self, dir, gens, chips):
        print(
            f"Moving {'Up' if dir == UP else 'Down'}, generators:{gens}, chips:{chips}"
        )
        size = len(gens) + len(chips)
        if dir == UP and size == 1:
            print("***************")
        assert 0 < size < 3 , "move takes 1 or 2 items"
        dest = self.flr + dir
        for gen in gens:
            self.gens().remove(gen)
            self.gens(dest).append(gen)
        for chip in chips:
            self.chips().remove(chip)
            self.chips(dest).append(chip)
        self.count += 1
        self.flr = dest
        self.display()
        self.is_valid()


def isolate_chips_on_1st(facility):
    # assumes lift on 1st, leaves it on 2nd
    match facility.by_matched():
        case ([], [pair], []):
            facility.move(UP, [pair], [pair])
            return pair


def clear_most_from_3rd(facility, chap):
    # assumes lift on 2nd, leaves on 2nd
    while True:
        match facility.by_matched(2):
            case ([], [], [chip1, chip2]):
                facility.move(UP, [chip1, chip2], [])
                facility.move(UP, [chip1], [chip1])
                facility.move(DOWN, [chip1], [])
                facility.move(UP, [chip1, chip2], [])
                facility.move(DOWN, [chip2], [])
                facility.move(DOWN, [chip2], [])
                facility.move(DOWN, [chap], [chap])
                facility.move(UP, [chap], [])
                return None, chip2
            case ([], [], [chip, _, *_]):
                facility.move(UP, [], [chap])
                facility.move(DOWN, [], [chip, chap])
            case _:
                raise RuntimeError("oops")


def move_pairs_from_2nd_to_4th(facility, chap, leading_chip=None):
    def move_pair(pair):
        if not leading_chip:
            facility.move(UP, [pair], [pair])
            facility.move(DOWN, [pair], [])
        facility.move(UP, [chap, pair], [])
        facility.move(UP, [chap, pair], [])
        facility.move(DOWN, [pair], [])
        facility.move(UP, [pair], [pair])
        facility.move(DOWN, [chap], [])
        facility.move(DOWN, [chap], [])

        
    if leading_chip:
        move_pair(leading_chip)   
        leading_chip = None
    _, pairs, _ = facility.by_matched()
    for pair in pairs:
        move_pair(pair)


def end(facility, chap):
    facility.move(DOWN, [chap], [])
    facility.move(UP, [chap], [chap])
    facility.move(UP, [chap], [chap])
    facility.move(UP, [chap], [chap])


def part1(facility, args, p1_state):
    facility.display()
    chaperone = isolate_chips_on_1st(facility)
    rmn_gen, rmn_chip = clear_most_from_3rd(facility, chaperone)
    assert not rmn_gen
    move_pairs_from_2nd_to_4th(facility, chaperone, rmn_chip)
    end(facility, chaperone)
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
