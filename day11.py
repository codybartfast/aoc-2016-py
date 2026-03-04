#  Day 11
#  ======
#
#  Part 1: 33
#  Part 2: 57
#
#  Timings
#  ---------------------
#    Parse:     0.000098
#   Part 1:    24.364271
#   Part 2:  2606.802769
#  Elapsed:  2631.167250

from itertools import combinations, zip_longest
import re

UP = +1
DOWN = -1


def parse(text):
    rx = re.compile(r"(\w+)(?:-\w+)? (generator|microchip)")

    def parse_line(line):
        floor = [[], []]
        for material, type in rx.findall(line):
            floor[0 if type == "generator" else 1].append(material[:2].title())
        floor[0].sort(), floor[1].sort()
        return floor

    floors = [parse_line(line) for line in (text.splitlines())]
    return Facility(floors, 0, 0)


class State:
    def __init__(self, max_moves):
        self.known = {}
        self.facility_count = 0
        self.max_moves = max_moves


class Facility:
    def __init__(self, floors, flr, count):
        self.floors = floors
        self.size = len(floors)
        self.flr = flr
        self.count = count

    def display(self):
        print(self.signature())
        print(f"count: {self.count}")

    def signature(self):
        lines = [
            f"{'E' if i == self.flr else ' '} {floor}"
            for i, floor in enumerate(self.floors)
        ]
        lines.reverse()
        return "\n".join(lines)

    def copy(self):
        n_floors = [(list(gens), list(chips)) for [gens, chips] in self.floors]
        return Facility(n_floors, self.flr, self.count)

    def done(self):
        return not any(gens or chips for gens, chips in self.floors[:-1])

    def is_valid(self):
        for floor in self.floors:
            if floor[1] and floor[0] and any(kind not in floor[0] for kind in floor[1]):
                assert False  # Invalid State
        return True

    def floor(self, flr=None):
        if flr is None:
            flr = self.flr
        return self.floors[flr]

    def lower(self):
        if self.flr == 0:
            return None
        return self.floors[self.flr - 1]

    def upper(self):
        flr = self.flr + 1
        if flr == self.size:
            return None
        return self.floors[flr]

    def grouped(self, flr=None):
        gens, chips = self.floor(flr)
        return (gens, [el for el in gens if el in chips], chips)

    def elevator_canditates(self):
        gens, pairs, chips = self.grouped()
        yield from ((list(g), []) for g in combinations(gens, 2))
        if pairs:
            yield (pairs[:1], pairs[:1])
        yield from (([], list(c)) for c in combinations(chips, 2))
        yield from (([g], []) for g in gens)
        yield from (([], [c]) for c in chips)

    def move(self, dir, elevator):
        # print("MOVEing", dir, elevator)
        gens_from, chips_from = self.floors[self.flr]
        self.flr += dir
        gens_to, chips_to = self.floors[self.flr]
        gens_x, chips_x = elevator
        for gen in gens_x:
            gens_from.remove(gen)
            gens_to.append(gen)
        for chip in chips_x:
            chips_from.remove(chip)
            chips_to.append(chip)
        gens_to.sort()
        chips_to.sort()
        self.count += 1

    @staticmethod
    def is_valid_floor(floor):
        gens, chips = floor
        rslt = not (gens and chips and any(chip for chip in chips if not chip in gens))
        # print("Valid? ", gens, chips, rslt)
        return rslt

    @staticmethod
    def floor_is_valid_with(floor, elev):
        gens, chips = floor
        x_gens, x_chips = elev
        return Facility.is_valid_floor((gens + x_gens, chips + x_chips))

    @staticmethod
    def floor_is_valid_without(floor, elev):
        gens, chips = floor
        x_gens, x_chips = elev
        return Facility.is_valid_floor(
            (
                [g for g in gens if g not in x_gens],
                [c for c in chips if c not in x_chips],
            )
        )


def movin_on_up(facility: Facility, state: State):
    sig = facility.signature()
    if state.known.get(sig, 10**18) <= facility.count:
        return

    if facility.count >= state.max_moves:
        return

    state.known[sig] = facility.count

    if facility.done():
        yield facility.count
        state.max_moves = facility.count
        return

    candidates = list(facility.elevator_canditates())
    allow_leave = [
        cand
        for cand in candidates
        if facility.floor_is_valid_without(facility.floor(), cand)
    ]
    upper = facility.upper()
    lower = facility.lower()
    allow_up = (
        [
            (UP, cand)
            for cand in allow_leave
            if facility.floor_is_valid_with(upper, cand)
        ]
        if upper
        else []
    )
    allow_down = (
        [
            (DOWN, cand)
            for cand in reversed(allow_leave)
            if facility.floor_is_valid_with(lower, cand)
        ]
        if lower
        else []
    )
    elevators = [
        elev
        for pair in zip_longest(allow_up, allow_down, fillvalue=None)
        for elev in pair
        if elev
    ]
    for dir, elev in elevators:
        new_facility = facility.copy()
        new_facility.move(dir, elev)
        state.facility_count += 1
        yield from movin_on_up(new_facility, state)


def part1(facility, args, p1_state):
    state = State(40)
    return min(movin_on_up(facility, state))


def part2(facility, args, p1_state):
    gens, chips = facility.floor()
    gens.extend(["El", "Di"])
    chips.extend(["El", "Di"])

    state = State(65)
    return min(movin_on_up(facility, state))


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
