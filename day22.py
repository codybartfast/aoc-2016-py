import re


def parse(text):
    digits = re.compile(r"\d+")

    def parse_line(line):
        nums = list(map(int, digits.findall(line)))
        return (nums[0], nums[1]), [nums[3], nums[4]]

    dfs = [parse_line(line) for line in text.splitlines()[2:]]
    width = max(x for (x, _), _ in dfs) + 1
    height = max(y for (_, y), _ in dfs) + 1

    return tuple(
        (tuple((dfs[x * height + y][1] for x in range(width))) for y in range(height))
    )


def totals(disks):
    total_used = sum(used for used, _ in disks)
    total_avail = sum(avail for _, avail in disks)
    return total_used, total_avail


def viable_count(disks):
    all = [disk for row in disks for disk in row]
    count = 0
    for i in range(len(all)):
        u1, a1 = all[i]
        for j in range(i + 1, len(all)):
            u2, a2 = all[j]
            if 0 < u1 <= a2:
                count += 1
            if 0 < u2 <= a1:
                count += 1
    return count


def part1(disks, args, p1_state):
    return viable_count(disks)


def part2(disks, args, p1_state):
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
