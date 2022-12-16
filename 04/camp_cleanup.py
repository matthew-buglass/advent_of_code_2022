with open('camp_clean_input.txt', 'r') as f:
    elf_pairs = [l.strip('\n').split(',') for l in f.readlines()]
    elf_pair_min_max = [[p[0].split('-'), p[1].split('-')] for p in elf_pairs]
    elf_pair_ranges = [[set(range(int(a[0]), int(a[1]) + 1)), set(range(int(b[0]), int(b[1]) + 1))] for a, b in
                       elf_pair_min_max]

# pt 1
elf_pair_range_inter = [r[0].intersection(r[1]) for r in elf_pair_ranges]
one_contained_in_other = [len(elf_pair_range_inter[i]) == len(elf_pair_ranges[i][0]) or
                          len(elf_pair_range_inter[i]) == len(elf_pair_ranges[i][1]) for
                          i in range(len(elf_pair_range_inter))]
print("Number of completely overlapping shifts: {}".format(one_contained_in_other.count(True)))

# pt 1
any_overlap = [len(elf_pair_range_inter[i]) != 0 for i in range(len(elf_pair_range_inter))]
print("Number of overlapping shifts: {}".format(any_overlap.count(True)))
