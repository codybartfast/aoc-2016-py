import array
from itertools import permutations

# On Day 22 I started going down what would have been a horrible brute force
# path and looked at arrary.array, so I'm using here out of curiosity, but I
# suspect it's overkill


class HVAC:
    def __init__(self, plan, dimensions):
        self.plan = plan
        self.dimensions = dimensions

    def __str__(self):
        w, h = self.dimensions
        plan = self.plan
        grid = ["".join(chr(plan[w * y + x]) for x in range(w)) for y in range(h)]
        # grid = ["".join("█" if (c := chr(plan[w * y + x])) == "#" else c for x in range(w)) for y in range(h)]
        grid.append(f"[{w} x {h}]")
        return "\n".join(grid)


def parse(text):
    lines = text.splitlines()

    plan = array.array("B")
    for line in lines:
        plan.extend(map(ord, line))

    return HVAC(plan, (len(lines[0]), len(lines)))


def find_nothing(hvac: HVAC):
    nothing = ord("0")
    w, _ = hvac.dimensions
    for i, b in enumerate(hvac.plan):
        if b == nothing:
            return i
            # return (i % w, i // w)


def distances_from(hvac: HVAC, start_idx, start_label):
    plan = hvac.plan
    w, _ = hvac.dimensions
    diffs = [-w, -1, 1, w]

    edge = [start_idx]
    known = set(edge)
    distances = []
    dist = 0
    while edge:
        dist += 1
        new_edge = []
        for e in edge:
            for diff in diffs:
                i = e + diff
                b = plan[i]
                if b != 0x23:  # '#'
                    if i not in known:
                        known.add(i)
                        new_edge.append(i)
                        if 0x30 <= b <= 0x39:  # '0' - '9'
                            distances.append(((start_label, chr(b)), (i, dist)))
        edge = new_edge

    return distances


def find_distances(hvac):
    distances = {}
    zero = find_nothing(hvac)
    dists_from_start = distances_from(hvac, zero, "0")
    distances.update((pair, dist) for pair, (_, dist) in dists_from_start)
    poi = [(idx, end) for (_, end), (idx, dist) in dists_from_start]

    for poi_idx, poi_label in poi:
        distances.update(
            (pair, dist) for pair, (_, dist) in distances_from(hvac, poi_idx, poi_label)
        )

    return distances


def find_route(distances, poi):
    # print(distances, poi)
    min = 10**18
    for route in permutations(poi):
        dist = distances['0', route[0]]
        dist += sum(distances[route[i], route[i + 1]] for i in range(len(route) - 1))
        if dist < min:
            min = dist
    return min


def part1(hvac, args, p1_state):
    distances = find_distances(hvac)
    poi = set(p for p, _ in distances.keys() if p != '0')
    return find_route(distances, poi)


def part2(hvac, args, p1_state):
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
