def parse(text):
    return int(text)

def part1(size, args, p1_state):
    print(f"\n{size}\n")
    circle = [[i - 1, i + 1] for i in range(size)]
    circle[0][0] = size - 1
    circle[-1][1] = 0

    i = 0
    elf = circle[i]
    while elf[0] != i:
        next = circle[elf[1]]    
        circle[next[1]][0] = i
        elf[1] = (i := next[1])
        elf = next
    return i + 1


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
