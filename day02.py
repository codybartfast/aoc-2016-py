def parse(text):
    return text.splitlines()

keypad = ["123", "456", "789"]

def press_buttons(x, y, instrs):
    keys = []
    for seq in instrs:
        for dir in seq:
            match dir:
                case "U":
                    y = max(0, y - 1)
                case "R":
                    x = min(2, x + 1)
                case "D":
                    y = min(2, y + 1)
                case "L":
                    x = max(0, x - 1)
        keys.append(keypad[y][x])
    return keys
        

def part1(data, args, state_for_part2):
    print(f"{data}\n\n")
    return press_buttons(1, 1, data)


def part2(data, args, state_from_part1):
    return "ans2"


def jingle(filename=None, filepath=None, text=None, extra_args=None):
    import sack

    text = text if text else sack.read_input(filename, filepath)
    sack.present(text, extra_args, parse, part1, part2)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    extra_args = sys.argv[1:] if len(sys.argv) > 2 else None
    jingle(filename=filename, extra_args=extra_args)
