import decimal
import math
"""
- Starting items
    - Order matters
    - Your worry level of item in monkey's hands
- Operation is change in worry level during inspection
- Test is monkey's reaction to new worry level
- Monkeys take turns
- Monkey inspects and throws all of its items at once
- Order of ops
    - Monkey inspects item
    - Worry level changes through operation
    - Worry level is divided by 3, rounded down, from relief
    - Monkey tests worry level
    - Monkey passes
"""

c = decimal.getcontext()
c.prec = decimal.MAX_PREC
c.Emax = decimal.MAX_EMAX
c.Emin = decimal.MIN_EMIN
c.traps[decimal.Inexact] = 1


class Operation:
    def __init__(self, desc, op, y, remainder_to_test=None):
        self.op = op
        self.desc = desc
        self.y = y
        self.remainder_to_test = remainder_to_test

    def __str__(self):
        return self.desc

    def run(self, a):
        if self.remainder_to_test is not None:
            res = self.op(a, self.y)
            return res == self.remainder_to_test
        else:
            return self.op(a, self.y)


class Monkey:
    def __init__(self, name, items, operation, logic_test, true_target=None, false_target=None):
        self.name = name
        self.items = items
        self.operation = operation
        self.logic_test = logic_test
        self.true_target = true_target
        self.false_target = false_target
        self.inspected_items = 0

    def __str__(self):
        return self.name

    def set_targets(self, true_target=None, false_target=None):
        self.true_target = true_target
        self.false_target = false_target

    def add_item(self, item_worry):
        self.items.append(item_worry)

    def inventory(self):
        return f'{self.name}: {", ".join([str(i) for i in self.items])}'

    def _inspect(self, verbose, calm_function):
        old = self.items[0]
        new = self.operation.run(old)
        calmed = calm_function(new)
        passed = self.logic_test.run(calmed)

        if passed:
            self.true_target.add_item(calmed)
        else:
            self.false_target.add_item(calmed)

        self.items.pop(0)
        self.inspected_items += 1

        if verbose:
            print(f'{self.name} inspects an item with worry level {old}\n'
                  f'\tWorry level is {self.operation.desc} to {new}\n'
                  f'\tMonkey gets bored. Worry is divided by 3 to {calmed}\n'
                  f'\tCurrent worry level is {"not" if not passed else ""} {self.logic_test.desc}\n'
                  f'\tItem with worry level {calmed} is passed to {self.true_target.name if passed else self.false_target.name}\n')

    def inspect_all(self, calm_function, verbose=False):
        for _ in range(len(self.items)):
            self._inspect(verbose, calm_function)


def run_tests(filename):
    monkeys = []
    divisors = []
    with open(filename, 'r') as f:
        target_to_align = {}
        input_lines = f.readlines()
        for i in range(0, len(input_lines), 7):
            name = input_lines[i].strip().rstrip(':')
            num = int(name.lstrip('Monkey '))
            items = [decimal.Decimal(i) for i in input_lines[i+1].strip().lstrip('Starting items: ').replace(' ', '').split(',')]
            op_string = input_lines[i+2].strip().replace('Operation: new = ', '')
            log_des = input_lines[i+3].strip().lstrip('Test: ')
            div_num = int(log_des.lstrip('divisible by '))
            true_tar_idx = int(input_lines[i+4].strip().lstrip('If true: throw to monkey '))
            false_tar_idx = int(input_lines[i + 5].strip().lstrip('If false: throw to monkey '))

            target_to_align[num] = (true_tar_idx, false_tar_idx)

            op_parts = op_string.split()
            if op_parts[0] == op_parts[-1] == 'old':
                if op_parts[1] == '*':
                    operation = Operation(desc=op_string, op=lambda x, y: x * x, y=0)
                else:
                    raise ValueError(f"expected equation doesn't match {op_string}")
            else:
                if op_parts[1] == '*':
                    operation = Operation(desc=op_string, op=lambda x, y: x * y, y=int(op_parts[-1]))
                elif op_parts[1] == '+':
                    operation = Operation(desc=op_string, op=lambda x, y: x + y, y=int(op_parts[-1]))

            logic_test = Operation(desc=log_des, op=lambda x, y: x % y, y=div_num, remainder_to_test=0)
            divisors.append(div_num)
            monkey = Monkey(name, items, operation, logic_test)
            monkeys.append(monkey)

        for key, val in target_to_align.items():
            monkeys[key].set_targets(monkeys[val[0]], monkeys[val[1]])

    rounds = 10000
    verbose = False
    for r in range(rounds):
        for mon in monkeys:
            if verbose:
                print(f'{"=" * 10} {mon} {"=" * 10}')
            mon.inspect_all(verbose=verbose, calm_function=lambda x: x % math.lcm(*divisors))

        if r % 100 == 0:
            print(f'\n{"=" * 10} After round {r + 1} {"=" * 10}')
            for mon in monkeys:
                print(f'{mon} inspected items {mon.inspected_items} times')

    most_active = 0
    second_most_active = 0
    for mon in monkeys:
        print(f'{mon} inspected items {mon.inspected_items} times')
        if mon.inspected_items > most_active:
            second_most_active = most_active
            most_active = mon.inspected_items
        elif mon.inspected_items > second_most_active:
            second_most_active = mon.inspected_items

    print(f'{most_active} * {second_most_active} = {most_active * second_most_active}')


# testing
run_tests('monkey_in_the_middle_test_input.txt')


# Actual work
run_tests('monkey_in_the_middle_input.txt')
