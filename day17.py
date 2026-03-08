from hashlib import md5

DIRS = [("U", (0, -1)), ("D", (0, 1)), ("L", (-1, 0)), ("R", (1, 0))]


def parse(text):
    return text.encode()


def next_paths(paths):
    npaths = []
    vpaths = []
    for path in paths:
        (x, y), steps, hash = path
        for (dir, (dx, dy)), hash_char in zip(DIRS, hash.hexdigest()):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 4 and 0 <= ny < 4 and hash_char in "bcdef":
                nhash = hash.copy()
                nhash.update(dir.encode())
                (npaths if (nx, ny) != (3, 3) else vpaths).append(
                    ((nx, ny), steps + [dir], nhash)
                )
    return npaths, vpaths


def explore(code):
    start = ((0, 0), [], md5(code))
    paths = [start]
    while paths:
        # print(paths)
        paths, vpaths = next_paths(paths)
        if vpaths:
            yield vpaths


def part1(code, args, p1_state):
    explore_it = iter(explore(code))
    p1_state.value = explore_it
    return "".join(next(explore_it)[0][1])


def part2(data, args, p1_state):
    vault_paths_list = list(p1_state.value)
    last = vault_paths_list[-1][-1]
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
