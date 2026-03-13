def parse(text):
    def parse_line(line):
        parts = line.split()
        match parts:
            case ["swap", "position", x, "with", "position", y]:
                return ("swap_pstn", int(x), int(y))
            case ["swap", "letter", x, "with", "letter", y]:
                return ("swap_ltr", x, y)
            case ["rotate", "left", x, _]:
                return ("rotate", int(x))
            case ["rotate", "right", x, _]:
                return ("rotate", -int(x))
            case ["rotate", "based", "on", "position", "of", "letter", x]:
                return ("rot_on_ltr_pstn", x)
            case ["reverse", "positions", x, "through", y]:
                return ("reverse", int(x), int(y))
            case ["move", "position", x, "to", "position", y]:
                return ("move", int(x), int(y))
            case _:
                assert False, parts

    return [parse_line(line) for line in text.splitlines()]


def based_on(size):
    return [((1 + x + x + (x >= 4)) % size) for x in range(size)]


def apply(operations, word):
    words=[word[:]]
    for op in operations:
        match op:
            case "swap_pstn", x, y:
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "swap_ltr", a, b:
                x = word.index(a)
                y = word.index(b)
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "rotate", n:
                word = word[n:] + word[:n]
            case "rot_on_ltr_pstn", a:
                x = word.index(a)
                n = -((1 + x + (x >= 4)) % len(word))
                # print(n, based_on(len(word))[x])
                word = word[n:] + word[:n]
            case "reverse", x, y:
                assert x < y
                word[x : y + 1] = word[x : y + 1][::-1]
            case "move", x, y:
                a = word.pop(x)
                word.insert(y, a)
            case _:
                assert False, op
        words.append(word[:])
    return words


def unapply(operations, word, based_on_map):
    for op in operations:
        match op:
            case "swap_pstn", x, y:
                # unchanged
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "swap_ltr", a, b:
                # unchanged
                x = word.index(a)
                y = word.index(b)
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "rotate", n:
                n = -n  #
                word = word[n:] + word[:n]
            case "rot_on_ltr_pstn", a:
                x = word.index(a)
                orig_x = based_on_map.index(x)
                n = (x - orig_x) % len(word)
                word = word[n:] + word[:n]

                # n = -((1 + x + (x >= 4)) % len(word))
                # word = word[n:] + word[:n]
            case "reverse", x, y:
                x, y = (x, y) if x < y else (y, x)  #
                word[x : y + 1] = word[x : y + 1][::-1]
            case "move", x, y:
                # unchanged
                a = word.pop(x)
                word.insert(y, a)
            case _:
                assert False, op
        # print("".join(word), op, "\n")
    return word


def part1(operations, args, p1_state):
    word = list("abcdefgh")
    words = apply(operations, word)
    return "".join(words[-1])


def part2(operations, args, p1_state):
    word = list("fbgdceah")
    # word = list("abcdefgh")
    # fwd_words = apply(operations, word)
    # last_word = fwd_words[-1]
    # print(last_word)
    # word = last_word

    based_on_destinations = based_on(len(word))
    assert len(based_on_destinations) == len(set(based_on_destinations))
    
    while operations:
        # assert word == fwd_words.pop()
        op = operations.pop()
        # print(word, op, end=" => ")
        match op:
            case "swap_pstn", x, y:
                # unchanged
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "swap_ltr", a, b:
                # unchanged
                x = word.index(a)
                y = word.index(b)
                t = word[x]
                word[x] = word[y]
                word[y] = t
            case "rotate", n:
                n = -n  #
                word = word[n:] + word[:n]
            case "rot_on_ltr_pstn", a:
                x = word.index(a)
                orig_x = based_on_destinations.index(x)
                n = (x - orig_x) % len(word)
                word = word[n:] + word[:n]

                # n = -((1 + x + (x >= 4)) % len(word))
                # word = word[n:] + word[:n]
            case "reverse", x, y:
                x, y = (x, y) if x < y else (y, x)  #
                word[x : y + 1] = word[x : y + 1][::-1]
            case "move", x, y:
                a = word.pop(y)
                word.insert(x, a)
            case _:
                assert False, op
        # print(word, "expected", fwd_words[-1])         
    return "".join(word)


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
