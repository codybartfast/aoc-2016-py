#  Day 11
#  ======
#
#  Part 1: 33
#  Part 2: 57
#
#  Timings
#  ---------------------
#    Parse:     0.000096
#   Part 1:     1.518925
#   Part 2:     5.724690
#  Elapsed:     7.243815

from itertools import combinations, islice
import re


# Bigger number here slows search but reduces chance of missing answer
MAX_FAC = 2**12


def parse(text):
    rx = re.compile(r"(\w+)(?:-\w+)? (generator|microchip)")

    def parse_line(line):
        floor = [[], []]
        for material, type in rx.findall(line):
            floor[0 if type == "generator" else 1].append(material[:2].title())
        floor[0].sort(), floor[1].sort()
        return floor

    floors = [parse_line(line) for line in (text.splitlines())]
    return (0, floors)


def signature(facility):
    e, floors = facility
    return e, tuple(
        (tuple(sorted(floor[0])), tuple(sorted(floor[1]))) for floor in floors
    )


def is_valid(facility):
    for floor in facility[1]:
        if floor[0] and floor[1] and any(elm not in floor[0] for elm in floor[1]):
            return False
    return True


def is_done(facility):
    e, floors = facility
    return (e == len(floors) - 1) and not any(
        gens or chips for gens, chips in floors[:-1]
    )


def score(facility):
    scr = 0
    for i, (gens, chips) in enumerate(facility[1]):
        scr += (i + 1) * sum(1 for elm in gens if elm in chips)
    return scr


def loads(facility):
    e, floors = facility
    gens, chips = floors[e]
    pairs = [elm for elm in gens if elm in chips]
    yield from ((list(g), []) for g in combinations(gens, 2))
    if pairs:
        yield (pairs[:1], pairs[:1])
    yield from (([], list(c)) for c in combinations(chips, 2))
    yield from (([g], []) for g in gens)
    yield from (([], [c]) for c in chips)


def move(old_floors, load, _from, _to):
    floors = [(list(gens), list(chips)) for [gens, chips] in old_floors]
    f_gens, f_chips = floors[_from]
    x_gens, x_chips = load
    t_gens, t_chips = floors[_to]
    for gen in x_gens:
        f_gens.remove(gen)
        t_gens.append(gen)
    for chip in x_chips:
        f_chips.remove(chip)
        t_chips.append(chip)
    return (_to, floors)


def next_facilities(facility):
    e, floors = facility
    if e < len(floors) - 1:
        yield from (move(floors, load, e, e + 1) for load in loads(facility))
    if e > 0:
        yield from (move(floors, load, e, e - 1) for load in loads(facility))


def next_generation(facilities, known: set):
    for facility in facilities:
        for next in next_facilities(facility):
            if is_valid(next) and (sgn := signature(next)) not in known:
                known.add(sgn)
                yield next


def dup_head(iter):
    head = next(iter)
    yield head
    yield head
    yield from iter


def search(facility):
    facilities = [facility]
    count = 0
    known = set()
    while True:
        count += 1
        facilities = next_generation(facilities, known)
        facilities = sorted(facilities, key=score, reverse=True)
        facilities = islice(facilities, MAX_FAC)
        dup_headed = dup_head(facilities)
        head = next(dup_headed)
        if is_done(head):
            return count
        facilities = dup_headed


def part1(facility, args, p1_state):
    return search(facility)


def part2(facility, args, p1_state):
    gens, chips = facility[1][0]
    gens.extend(["Di", "El"])
    chips.extend(["Di", "El"])
    return search(facility)


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
