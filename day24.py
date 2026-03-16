#  2016 Day 24
#  ===========
#
#  Part 1: 428
#  Part 2: 680
#
#  Timings
#  ---------------------
#    Parse:     0.000199
#   Part 1:     0.007976
#   Part 2:     0.000000
#  Elapsed:     0.008209


import array
from itertools import permutations


class HVAC:
    def __init__(self, plan, dimensions):
        self.plan = plan
        self.dimensions = dimensions

    def __str__(self):
        w, h = self.dimensions
        plan = self.plan
        grid = ["".join(chr(plan[w * y + x]) for x in range(w)) for y in range(h)]
        grid.append(f"[{w} x {h}]")
        return "\n".join(grid)


def parse(text):
    lines = text.splitlines()
    plan = array.array("B", [ord(c) for line in lines for c in line])

    return HVAC(plan, (len(lines[0]), len(lines)))


def find_nothing(hvac: HVAC):
    nothing = ord("0")
    w, _ = hvac.dimensions
    for i, b in enumerate(hvac.plan):
        if b == nothing:
            return i


def distances_from(hvac: HVAC, start_idx, start_label):
    plan = hvac.plan
    width, _ = hvac.dimensions
    deltas = [-width, -1, 1, width]

    edge = [start_idx]
    known = set(edge)
    distances = []
    dist = 0
    while edge:
        dist += 1
        new_edge = []
        for idx in edge:
            for delta in deltas:
                adj_idx = idx + delta
                byt = plan[adj_idx]
                if byt != 0x23 and adj_idx not in known:  # 0x23 = '#'
                    known.add(adj_idx)
                    new_edge.append(adj_idx)
                    if 0x30 <= byt <= 0x39:  # '0' - '9'
                        distances.append(((start_label, chr(byt)), (adj_idx, dist)))
        edge = new_edge
    return distances


def find_distances(hvac):
    zero_idx = find_nothing(hvac)
    dists_from_start = distances_from(hvac, zero_idx, "0")
    distances = dict((pair, dist) for pair, (_, dist) in dists_from_start)

    poi = [(idx, end) for (_, end), (idx, dist) in dists_from_start]
    for poi_idx, poi_label in poi:
        distances.update(
            (pair, dist) for pair, (_, dist) in distances_from(hvac, poi_idx, poi_label)
        )
    return distances


def find_shortest(distances, poi):
    min1 = 10**18
    min2 = 10**18
    for route in permutations(poi):
        dist1 = distances["0", route[0]]
        dist1 += sum([distances[route[i], route[i + 1]] for i in range(len(route) - 1)])
        if dist1 < min1:
            min1 = dist1
        dist2 = dist1 + distances[route[-1], "0"]
        if dist2 < min2:
            min2 = dist2
    return min1, min2


def part1(hvac, args, p1_state):
    distances = find_distances(hvac)
    poi = set(p for p, _ in distances.keys() if p != "0")
    min1, min2 = find_shortest(distances, poi)
    p1_state.value = min2
    return min1


def part2(hvac, args, p1_state):
    return p1_state.value


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
