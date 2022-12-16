# Each ruck:
#   2 large compartments
#   one item type per pack
#   first half = first compartment
# each char diff item
# each sack diff line
# priority a-Z = 1-52,

priority = "abcdefghijklmnopqrstuvwxyz"
priority = priority + priority.upper()

with open('rucksack_input.txt', 'r') as f:
    rucksacks = [l.strip('\n') for l in f.readlines()]

# PT 1
rucksack_comps = [[r[0:len(r)//2], r[len(r)//2:]] for r in rucksacks]
same_items = [set(r[0]).intersection(set(r[1])).pop() for r in rucksack_comps]
priorities = [priority.find(i) + 1 for i in same_items]
print('Sum of priorities: {}'.format(sum(priorities)))

# Pt 2
elf_groups = [rucksacks[i:i+3] for i in range(0, len(rucksacks), 3)]
group_badges = [set(e[0]).intersection(set(e[1])).intersection(set(e[2])).pop() for e in elf_groups]
badge_priorities = [priority.find(i) + 1 for i in group_badges]
print('Sum of Badge priorities: {}'.format(sum(badge_priorities)))
