import re


class Stack:
    def __init__(self, items=None, name=""):
        self.items = items or []
        self.name = name

    def __str__(self):
        return "{} : <-- {} |".format(self.name, ' - '.join(self.items))

    def pop(self):
        if len(self.items) > 0:
            item = self.items[0]
            self.items = self.items[1:]
            return item
        return None

    def push(self, item):
        self.items = [item] + self.items

    def peek(self):
        return self.items[0]


class MultiStack(Stack):
    def pop(self, num=1):
        if num == 1:
            return super(MultiStack, self).pop()
        elif len(self.items) <= num:
            items = self.items
            self.items = []
            return items
        else:
            items = self.items[0:num]
            self.items = self.items[num:]
            return items

    def push(self, items):
        if isinstance(items, str):
            super(MultiStack, self).push(items)
        else:
            self.items = items + self.items


def input_to_stacks(setup_str, use_multi=False):
    regex = r'\[[A-Z]\] |    '
    box_stack_arr = [re.findall(regex, r) for r in setup_str]
    num_cols = len(box_stack_arr[0])

    if use_multi:
        stacks = [MultiStack(name=str(i + 1)) for i in range(num_cols)]
    else:
        stacks = [Stack(name=str(i+1)) for i in range(num_cols)]

    box_stack_arr.reverse()
    for row in box_stack_arr:
        for col_num in range(len(row)):
            item = row[col_num]
            clean_item = item.strip().replace('[', '').replace(']', '')
            if clean_item != '':
                stacks[col_num].push(clean_item)

    return stacks


with open('supply_stack_input.txt', 'r') as f:
    setup = []

    line = f.readline()
    while line != '\n':
        setup.append(line.replace('\n', ' '))
        line = f.readline()

    instructions = [l.strip() for l in f.readlines()]

# pt 1 & 2
# creating the stacks
stacks = input_to_stacks(setup)
stacks_multi = input_to_stacks(setup, True)

for step in instructions:
    num, src_dst = step.lstrip('move ').split(' from ')
    src, dst = src_dst.split(' to ')

    num = int(num)
    src = int(src) - 1
    dst = int(dst) - 1

    for i in range(num):
        stacks[dst].push(stacks[src].pop())

    stacks_multi[dst].push(stacks_multi[src].pop(num))

print('\n\n\n')
print('\n'.join([str(s) for s in stacks]))
print('Top set: {}'.format(''.join([s.peek() for s in stacks])))

print('\n\n\n')
print('\n'.join([str(s) for s in stacks_multi]))
print('Top set: {}'.format(''.join([s.peek() for s in stacks_multi])))
