#  2016 Day 17
#  ===========
#
#  Part 1: RDRDUDLRDR
#  Part 2: 386
#
#  Timings
#  ---------------------
#    Parse:     0.000001
#   Part 1:     0.000060
#   Part 2:     0.039628
#  Elapsed:     0.039733


from hashlib import md5

DIRS = [(b"U", (0, -1)), (b"D", (0, 1)), (b"L", (-1, 0)), (b"R", (1, 0))]


def parse(text):
    return text.encode()


def next_paths(paths):
    new_paths = []
    vault_paths = []
    for path in paths:
        (x, y), steps, hash = path
        hexdigest = hash.hexdigest()
        for i in range(4):
            dir, (dx, dy) = DIRS[i]
            hash_char = hexdigest[i]
            nx, ny = x + dx, y + dy
            if 0 <= nx < 4 and 0 <= ny < 4 and hash_char in "bcdef":
                nhash = hash.copy()
                nhash.update(dir)
                (vault_paths if (nx, ny) == (3, 3) else new_paths).append(
                    ((nx, ny), steps + [dir], nhash)
                )
    return new_paths, vault_paths


def explore(code):
    start = ((0, 0), [], md5(code))
    paths = [start]
    while paths:
        paths, vault_paths = next_paths(paths)
        if vault_paths:
            yield vault_paths


def part1(code, args, p1_state):
    explore_it = iter(explore(code))
    p1_state.value = explore_it
    vault_path = next(explore_it)[0]
    return b"".join(vault_path[1]).decode()


def part2(code, args, p1_state):
    vault_paths_list = list(p1_state.value)
    last = vault_paths_list[-1][0]
    return len(last[1])


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
