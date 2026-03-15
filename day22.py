#  2016 Day 22
#  ===========
#
#  Part 1: 960
#  Part 2: 225
#
#  Timings
#  ---------------------
#    Parse:     0.001803
#   Part 1:     0.015357
#   Part 2:     0.000052
#  Elapsed:     0.017267


# This puzzle reminded me that these are infact puzzles, not pure coding
# exercises.  The main purpose of the Part 1 is misdirection.  At first sight it
# creates the impression that there are many different ways data could be
# doubled up on a disk creating multiple empty disks.  It also has us (or me)
# thinking we have to check there is room before any planned move.  Neither is
# really true.  The 960 viable moves is simply the number of 'regular' disks all
# of which could fit into the empty disk, movement to the empty disk is the only
# vialble move.  Further, the largest used value is less than the smallest size
# (ignoring very large disks) so any data can be moved to any disk.  In short
# the disk usage data is almost irrelevent except for identifying the very large
# disks and the empty disk.
#
# With hindsight there are a couple of clues.  First, the mumber of viable pairs
# which is quite small, there could have been nearly a million so 960 is
# suspiciously low, especially when we know there's an empty disk.  Second, is
# the diagram we see in Part 2.
#
#     (.) .  G
#      .  _  .
#      #  .  .
#
# If you ignore all the distractions then this is what the problem really is.


"""
(.) .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  G
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
 .  .  .  .  .  .  .  .  .  .  .  .  .  .  . [_] .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
"""

import re

COORD = 0
STATS = 1

USED = 0
AVAIL = 1


def parse(text):
    digits = re.compile(r"\d+")

    def parse_line(line):
        nums = list(map(int, digits.findall(line)))
        return (nums[0], nums[1]), [nums[3], nums[4]]

    dfs = [parse_line(line) for line in text.splitlines()[2:]]
    width = max(x for (x, _), _ in dfs) + 1
    height = max(y for (_, y), _ in dfs) + 1

    return tuple(
        (tuple((dfs[x * height + y] for x in range(width))) for y in range(height))
    )


def render(disks):
    h = len(disks)
    w = len(disks[0])
    max_x = w - 1

    def render_disk(disk):
        x, y = disk[COORD]
        u = disk[STATS][USED]
        if y == 0 and x == 0:
            return "(.)"
        if y == 0 and x == max_x:
            return " G "
        if u == 0:
            return "[_]"
        if u > 200:
            return " # "
        else:
            return " . "

    return "\n".join(
        "".join(render_disk(disks[y][x]) for x in range(w)) for y in range(h)
    )


def viable_count(disks):
    all = [disk[STATS] for row in disks for disk in row]
    count = 0
    for i in range(len(all)):
        used1, avail1 = all[i]
        for j in range(i + 1, len(all)):
            used2, avail2 = all[j]
            if 0 < used1 <= avail2:
                count += 1
            if 0 < used2 <= avail1:
                count += 1
    return count


def move_data(disks):
    h = len(disks)
    w = len(disks[0])
    max_x = w - 1
    empty_x, empty_y = next(
        disk[COORD]
        for y in range(h)
        for x in range(w)
        if (disk := disks[y][x])[STATS][USED] == 0
    )

    wall_y = 0
    while disks[wall_y][max_x][STATS][USED] < 200:
        wall_y += 1
    walls_end = max_x
    while disks[wall_y][walls_end][STATS][USED] >= 200:
        walls_end -= 1

    steps = 0
    # move empty left to walls end
    steps += empty_x - walls_end

    # move empty to top
    steps += empty_y

    # move empty right until left of Goal
    steps += w - 2 - walls_end

    # Goal moves into empty
    steps += 1

    # move empty in front of Goal and move Goal (and repeat)
    steps += 5 * (max_x - 1)

    return steps


def part1(disks, args, p1_state):
    return viable_count(disks)


def part2(disks, args, p1_state):
    return move_data(disks)


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
