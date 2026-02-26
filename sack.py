from pathlib import Path
import re
import sys

YEAR = "2016"


def get_day():
    filename = Path(sys._getframe(2).f_code.co_filename).name

    day_match = re.search(r"day(\d\d)", filename)
    if not day_match:
        raise RuntimeError(f"Couldn't get day from filename: {filename}")
    return day_match.group(1)


def get_filepath(file):
    if not file:
        file = "input"
    canonical = (
        Path(__file__).resolve().parent
        / "input"
        / YEAR
        / f"day{get_day()}"
        / (file + ".txt")
    )
    if canonical.is_file():
        return canonical
    other = Path(file)
    if other.is_file():
        return other
    print()
    print("Couldn't find input file.")
    print(f"Tried: '{canonical}'")
    print(f"  and: '{other.resolve()}'")
    return None


def present(text, extra_args, parse, part1, part2):
    import time

    def h_print(*args):
        print("# ", *args)

    class State:
        def __init__(self):
            self.ans1 = None
            self.value = None
    state = State()

    pc_start = time.perf_counter()
    day = get_day()

    title = f"Day {day}"

    print("\n")
    h_print(title)
    h_print("=" * len(title))
    h_print()

    pc_parse_before = time.perf_counter()
    data = parse(text)
    pc_parse_after = time.perf_counter()

    pc_part1_before = time.perf_counter()
    ans1 = part1(data, extra_args, state)
    pc_part1_after = time.perf_counter()
    h_print(f"Part 1: {ans1}")

    state.ans1 = ans1

    pc_part2_before = time.perf_counter()
    ans2 = part2(data, extra_args, state)
    pc_part2_after = time.perf_counter()
    h_print(f"Part 2: {ans2}")

    pc_stop = time.perf_counter()

    h_print()
    h_print("Timings")
    h_print("---------------------")
    h_print(f"  Parse: {pc_parse_after - pc_parse_before:12.6f}")
    h_print(f" Part 1: {pc_part1_after - pc_part1_before:12.6f}")
    h_print(f" Part 2: {pc_part2_after - pc_part2_before:12.6f}")
    h_print(f"Elapsed: {pc_stop - pc_start:12.6f}")
    print()
