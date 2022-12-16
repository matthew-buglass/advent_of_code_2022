#!/bin/python3

with open('calories.txt', 'r') as f:
    # Pt 1
    cal_lines = f.readlines()
    cal_lines = ''.join(cal_lines).split('\n\n')
    cal_lines = [elf.replace('\n', "+") for elf in cal_lines]
    total_cals = [eval(elf) for elf in cal_lines]
    print("Max Calories {}".format(max(total_cals)))

    # Pt 2
    total_cals.sort(reverse=True)
    print("Sum of top three elves: {}".format(sum(total_cals[0:3])))


