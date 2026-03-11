#  2016 Day 19
#  ===========
#
#  Part 1: 1834471
#  Part 2: 1420064
#
#  Timings
#  ---------------------
#    Parse:     0.000001
#   Part 1:     3.450346
#   Part 2:     3.491087
#  Elapsed:     6.941536


def parse(text):
    return int(text)


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


def part1(size, args, p1_state):
    return part1_linked_list(size)


def part2(size, args, p1_state):
    # return
    return part2_linked_list(size)



# 
# Linked Array
#
# This is simulating a linked list type approach by having pairs in array with
# prev and next and the array index being the identity.


#   Part 1:     0.527072


def part1_next_array(size):
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


#   Part 2: 55013.937808 (15.28 hours)
#
#   I know this is O(n^2) but was still shocked how slow this was compared to
#   the prev F# soln which similar, quadratic, and took around 4 secs. So while
#   it was running I wrote the tree based solution and then played around with
#   other listy solutions to see where the perf was being lost.


def part2_next_array(size):
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

        # print(player_id, "  removing:", target_id)
        player = circle[player]
        remaining -= 1
    return player + 1


# Shrinking List
#
# Nice simple list where just delete elves :'(  This is O(n2) for both Part 1
# and Part 2, but because list is using memmove it's much faster at this scale.


#   Part 1:   390.332638
#
#   This is slower than Part 2 because all the early pops are right at start
#   of list - so nearly whole list is being memmoved after each pop in the
#   early stages when list is longest.  So probably significant improvement in
#   speed if maybe 1) splice first half after second half and start in middle
#   or (more fuss, but I suspect bigger adv) 2) reverse circle and 'logic' so
#   first pop is circle[-2].  But neither's going to help with Part 2.


def part1_pop(size):
    circle = [i for i in range(size)]
    player_idx = 0
    while size > 1:
        target_idx = (player_idx + 1) % size
        # print(circle[player_idx], "  removing:", circle[target_idx], circle)
        circle.pop(target_idx)
        player_idx = target_idx
        size -= 1
    return circle[0] + 1


#   Part 2:   294.288204


def part2_pop(size):
    circle = [i for i in range(size)]
    player_idx = 0
    while size > 1:
        target_idx = (player_idx + (size // 2)) % size
        # print(circle[player_idx], "  removing:", circle[target_idx], circle)
        circle.pop(target_idx)
        size -= 1
        if player_idx < target_idx:
            player_idx += 1
        player_idx %= size
    return circle[0] + 1


# Linked List
#


class Elf:
    __slots__ = ("elf", "next")

    def __init__(self, elf):
        self.elf = elf
        self.next = None

    def __repr__(self):
        return str(self.elf)


#   Part 1:     0.432310

def part1_linked_list(size):
    first = Elf(1)
    prev = first
    for elf_id in range(2, size + 1):
        new_elf = Elf(elf_id)
        prev.next = new_elf
        prev = new_elf
    prev.next = first

    player = first
    while player.next != player:
        target = player.next
        # print(player.elf, "  Removing:", target.elf)
        player.next = target.next
        player = player.next
        
    return player.elf


#   Part 2: 35492.440158 (9.86 hours)
#
def part2_linked_list(size):
    first = Elf(1)
    prev = first
    for elf_id in range(2, size + 1):
        new_elf = Elf(elf_id)
        prev.next = new_elf
        prev = new_elf
    prev.next = first

    player = first
    while size > 1:
        before_target = player
        dist = (size // 2) - 1
        for _ in range(dist):
            before_target = before_target.next
        # print(player.elf, "  Removing:", target.elf)
        target = before_target.next
        after_target = target.next
        before_target.next = after_target
        player = player.next
        size -= 1
    return player.elf


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

