#  Day 10
#  ======
#
#  Part 1: 147
#  Part 2: 55637
#
#  Timings
#  ---------------------
#    Parse:     0.000149
#   Part 1:     0.000019
#   Part 2:     0.000047
#  Elapsed:     0.000259


BOT_VALUE = 0
BOT_LOW = 1
BOT_HIGH = 2


def parse(text):
    values_data = []
    bots_data = []
    for line in text.splitlines():
        parts = line.split()
        match line[0]:
            case "v":
                values_data.append((int(parts[1]), int(parts[5])))
            case "b":
                bots_data.append(
                    (
                        int(parts[1]),
                        (parts[5][0], int(parts[6])),
                        (parts[10][0], int(parts[11])),
                    )
                )
    max_bot_id = max(bot[0] for bot in bots_data)
    bots = [None] * (max_bot_id + 1)
    all_dest = []
    pending = []
    for id, low, high in bots_data:
        bots[id] = [None, low, high]
        all_dest.append(low)
        all_dest.append(high)
    for val, id in values_data:
        if bots[id][BOT_VALUE] is None:
            bots[id][BOT_VALUE] = val
        else:
            pending.append((val, ("b", id)))
    max_out_id = max(dest[1] for dest in all_dest if dest[0] == "o")
    outputs = [[] for _ in range(max_out_id + 1)]
    assert len(pending) == 1
    return bots, outputs, pending[0]


def move_chip(bots, outputs, chip, dest):
    kind, id = dest
    if kind == "o":
        outputs[id].append(chip)
        if all(len(output) == 1 for output in outputs[:3]):
            yield outputs[0][0] * outputs[1][0] * outputs[2][0]
    else:
        assert kind == "b"
        bot = bots[id]
        if bot[BOT_VALUE] is None:
            bot[BOT_VALUE] = chip
        else:
            low, high = chip, bot[BOT_VALUE]
            if low > high:
                low, high = high, low
            if (low, high) == (17, 61):
                yield id
            bots[id][BOT_VALUE] = None
            yield from move_chip(bots, outputs, low, bot[BOT_LOW])
            yield from move_chip(bots, outputs, high, bot[BOT_HIGH])


def part1(data, args, p1_state):
    bots, outputs, (chip, dest) = data

    answers = move_chip(bots, outputs, chip, dest)
    p1_state.value = answers
    return next(answers)


def part2(data, args, p1_state):
    return next(p1_state.value)


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
