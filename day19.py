#  2016 Day 19
#  ===========
#
#  Part 1: 1834471
#  Part 2: 1420064
#
#  Timings
#  ---------------------
#    Parse:     0.000001
#   Part 1:     0.141588
#   Part 2:     0.413573
#  Elapsed:     0.555239


# There are five different solutions for this puzzle.  Basically because I made
# two mistakes.
#
# First for some reason I assumed my old 2016 F# solution was using brute force
# but was still completing in just a couple of seconds. It wasn't.  But based on
# this assumpiton I was trying to understand the (non-existent) 10,000x
# difference in performance.
#
# Second, I fixated on the approach "move player, find target" the tree
# solution made this quite fast (3 seconds) and I quite like it but a better
# appraoch is the one I actually used in F# which was "Move player, Move
# Target".
#
# Linked:
#     Using a single linked list this is erhaps the most obvious approach but
#     is catastrophically slow for Part2, over 5 hours.
#
# Array:
#     This is essentially the same idea but instead of objects there's just one
#     array with array[n] saying which elf comes after the elf n.  This is the
#     fastest for Part 1 but is almost as cataestrophic as Linked for Part 2.
#
# Pop:
#     This is still O(n^2) but since list.pop() is using memmove under the hood
#     it's about 60x faster, about 5 minutes instead of 5 hours.
#
# Tree:
#     This is O(n log n) using a tree structure to find and remove the target
#     each time, taking around 3 seconds to complete.
#
# Track:
#     This is the approach I used in F# previously.  It's linear, remove
#     Target, move Player, maybe move Target.  It takes around 1/2 a second.
#     It's not really applicable to Part 1.
#
#
#                    │     Part 1  │     Part 2
#           ─────────┼─────────────┼─────────────
#            Linked  │       0.39  │  22,578.64
#             Array  │       0.14  │  21,669.57
#               Pop  │     388.61  │     296.60
#              Tree  │       3.43  │       3.52
#             Track  │     ------  │       0.41
#


def parse(text):
    return int(text)


def part1(size, args, p1_state):
    if args:
        match args[0]:
            case "linked":
                solver = part1_linked
            case "array":
                solver = part1_array
            case "pop":
                solver = part1_pop
            case "tree":
                solver = part1_tree
            case "track":
                solver = part1_array
            case _:
                assert False
    else:
        solver = part1_array
    return solver(size)


def part2(size, args, p1_state):
    if args:
        match args[0]:
            case "linked":
                solver = part2_linked
            case "array":
                solver = part2_array
            case "pop":
                solver = part2_pop
            case "tree":
                solver = part2_tree
            case "track":
                solver = part2_track
            case _:
                assert False
    else:
        solver = part2_track
    return solver(size)


# Linked
###############################################################################


class Elf:
    __slots__ = ("elf", "next")

    def __init__(self, elf):
        self.elf = elf
        self.next = None

    def __repr__(self):
        return str(self.elf)


def elf_circle(size):
    first = Elf(1)
    prev = first
    for elf_id in range(2, size + 1):
        new_elf = Elf(elf_id)
        prev.next = new_elf
        prev = new_elf
    prev.next = first
    return first


def part1_linked(size):
    player = elf_circle(size)
    while player.next != player:
        target = player.next
        player.next = target.next
        player = player.next

    return player.elf


def part2_linked(size):
    player = elf_circle(size)
    while size > 1:
        before_target = player
        dist = (size // 2) - 1
        for _ in range(dist):
            before_target = before_target.next
        target = before_target.next
        after_target = target.next
        before_target.next = after_target
        player = player.next
        size -= 1
    return player.elf


# Array
###############################################################################


def part1_array(size):
    circle = [i + 1 for i in range(size)]
    circle[-1] = 0

    player = 0
    size -= 1
    while size:
        next = circle[player]
        nn = circle[next]
        circle[player] = nn
        player = nn
        size -= 1
    return player + 1


def part2_array(size):
    circle = [i + 1 for i in range(size)]
    circle[-1] = 0

    player = 0
    remaining = size
    while remaining > 1:
        before_target = player
        for _ in range((remaining // 2) - 1):
            before_target = circle[before_target]
        target = circle[before_target]
        after_target = circle[target]
        circle[before_target] = after_target
        player = circle[player]
        remaining -= 1
    return player + 1


# Pop
###############################################################################


def part1_pop(size):
    circle = [i for i in range(size)]
    player_idx = 0
    while size > 1:
        target_idx = (player_idx + 1) % size
        circle.pop(target_idx)
        player_idx = target_idx
        size -= 1
    return circle[0] + 1


def part2_pop(size):
    circle = [i for i in range(size)]
    player_idx = 0
    while size > 1:
        target_idx = (player_idx + (size // 2)) % size
        circle.pop(target_idx)
        size -= 1
        if player_idx < target_idx:
            player_idx += 1
        player_idx %= size
    return circle[0] + 1


# Tree
###############################################################################


class Tree:
    def __init__(self, items):
        l_size = len(items) // 2
        self.l_size = l_size
        if l_size > 2:
            self.left = Tree(items[:l_size])
        else:
            self.left = Leaf(items[:l_size])

        self.r_size = len(items) - l_size
        if self.r_size > 2:
            self.right = Tree(items[l_size:])
        else:
            self.right = Leaf(items[l_size:])

    def remove(self, i):
        if i < self.l_size:
            self.l_size -= 1
            return self.left.remove(i)
        else:
            i -= self.l_size
            assert i < self.r_size
            self.r_size -= 1
            return self.right.remove(i)

    def size(self):
        return self.l_size + self.r_size


class Leaf:
    def __init__(self, items):
        match len(items):
            case 1:
                self.right = items[0]
                self.l_size = 0
                self.r_size = 1
            case 2:
                self.left = items[0]
                self.right = items[1]
                self.l_size = 1
                self.r_size = 1
            case _:
                assert False

    def remove(self, i):
        if i < self.l_size:
            self.l_size -= 1
            return self.left
        else:
            i -= self.l_size
            assert i < self.r_size
            self.r_size -= 1
            return self.right

    def size(self):
        return self.l_size + self.r_size


def part1_tree(size):
    tree = Tree([i for i in range(1, size + 1)])
    pstn = 0
    while size > 1:
        target = (pstn + 1) % size
        tree.remove(target)
        size -= 1
        pstn = target % size
    return tree.remove(0)


def part2_tree(size):
    tree = Tree([i for i in range(1, size + 1)])
    pstn = 0
    while size > 1:
        target = (pstn + (size // 2)) % size
        tree.remove(target)
        size -= 1
        if pstn < target:
            pstn += 1
        pstn = pstn % size
    return tree.remove(0)


# Track
###############################################################################


def part2_track(size):
    player = elf_circle(size)
    before_target = player
    for _ in range(size // 2 - 1):
        before_target = before_target.next

    while size > 1:
        before_target.next = before_target.next.next
        if size % 2:
            before_target = before_target.next
        player = player.next
        size -= 1
    return player.elf


# Runner
###############################################################################


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
    else:
        print(sys.argv)
        print("\nUsage: day19.py [<file> [<method>]]")
