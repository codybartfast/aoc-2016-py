from hashlib import md5

DIRS = [("U", (0, -1)), ("D", (0, 1)), ("L", (-1, 0)), ("R", (1, 0))]

def parse(text):
    return text.encode()


def next_paths(paths, size):
    npaths = []
    for path in paths:
        (x, y), steps, hash = path
        for (dir, (dx, dy)), hash_char in zip(DIRS, hash.hexdigest()):
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and hash_char in "bcdef":
                nhash = hash.copy()
                nhash.update(dir.encode())
                npaths.append(((nx, ny), steps + [dir], nhash))
    return npaths
        
    


def part1(code, args, p1_state):
    size = 4
    end = (size - 1, size - 1)
    print(f"{code}\n\n")
    paths = [((0,0), [], md5(code))]
    v_paths = None
    while paths and not v_paths:
        # print(paths)
        paths = next_paths(paths, 4)
        v_paths = [path for path in paths if path[0] == end]
            

    return "".join(v_paths[0][1])


def part2(data, args, p1_state):
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
