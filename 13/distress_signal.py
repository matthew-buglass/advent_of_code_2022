'''
Problem Notes
    - input is list of received packets (scrambled)
    - need to decipher number of pairs of packets are in correct order
    - comapare 2 items at a time
        - first is "left" second is "right"
        - Both are ints, the lower comes first
            - If left lower than right, in correct order
            - If right lower than left, not in correct order
            - If both the same, keep looking
        - If both are lists, compare vals of each list
            - Same number patterns as before
            - If left list runs out first, correct order
            - If right list runs out first, incorrect order
            - If same length and vals don't reveal, keep looking
        - If only one is a list, convert the other to a one item list and retry
'''


from const import color


def comparison_test(left_item, right_item):
    # 1 == correct order
    # -1 == incorrect order
    # 0 == indeterminate
    if isinstance(left_item, int) and right_item is None:
        return -2
    elif left_item is None and isinstance(right_item, int):
        return 2
    elif isinstance(left_item, int) and isinstance(right_item, int):
        if left_item < right_item:
            return 1
        elif right_item < left_item:
            return -1

    return 0


def in_correct_order(left_item: list, right_item: list, verbose=False, leading_chars=''):
    if verbose:
        print(f'{leading_chars}- Compare {left_item} vs. {right_item}')

    for i in range(max(len(left_item), len(right_item))):
        sub_left = None if i >= len(left_item) else left_item[i]
        sub_right = None if i >= len(right_item) else right_item[i]

        # recursive cases
        if isinstance(sub_left, list) and isinstance(sub_right, list):
            result = in_correct_order(sub_left, sub_right, verbose, leading_chars+'\t')
        elif isinstance(sub_left, int) and isinstance(sub_right, list):
            if verbose:
                print(f'{leading_chars}\t- Mixed types. Converting {sub_left} to [{sub_left}]')

            sub_left = [sub_left]
            result = in_correct_order(sub_left, sub_right, verbose, leading_chars+'\t')
        elif isinstance(sub_left, list) and isinstance(sub_right, int):
            if verbose:
                print(f'{leading_chars}\t- Mixed types. Converting {sub_right} to [{sub_right}]')

            sub_right = [sub_right]
            result = in_correct_order(sub_left, sub_right, verbose, leading_chars+'\t')
        elif sub_left is None and isinstance(sub_right, list):
            result = 2
        elif isinstance(sub_left, list) and sub_right is None:
            result = -2
        # Base case
        else:
            result = comparison_test(sub_left, sub_right)

        if result == 1:
            if verbose and leading_chars == '':
                print(f'{leading_chars}\t- Left side is smaller. In correct order')
            return result
        elif result == -1:
            if verbose and leading_chars == '':
                print(f'{leading_chars}\t- Right side is smaller. Not in correct order')
            return result
        elif result == 2:
            if verbose and leading_chars == '':
                print(f'{leading_chars}\t- Left ran out of items. In correct order')
            return result
        elif result == -2:
            if verbose and leading_chars == '':
                print(f'{leading_chars}\t- Right side ran out of items. Not in correct order')
            return result


def merge_sort_lines(lines, verbose=False):
    # base cases
    if len(lines) == 1:
        return [lines[0]]
    elif len(lines) == 0:
        return []
    # recursive case
    else:
        new_lines = []
        mid_point = len(lines) // 2
        left = lines[0:mid_point]
        right = lines[mid_point:]

        left_sorted = merge_sort_lines(left)
        right_sorted = merge_sort_lines(right)

        if len(left_sorted) > 0 and len(right_sorted) > 0:
            left_item = left_sorted.pop(0)
            right_item = right_sorted.pop(0)

            while True:
                result = in_correct_order(eval(left_item), eval(right_item), verbose)

                if result > 0:
                    new_lines.append(left_item)
                    try:
                        left_item = left_sorted.pop(0)
                    except IndexError:
                        new_lines.append(right_item)
                        break
                else:
                    new_lines.append(right_item)
                    try:
                        right_item = right_sorted.pop(0)
                    except IndexError:
                        new_lines.append(left_item)
                        break

        new_lines += left_sorted
        new_lines += right_sorted

        return new_lines


def run_tests(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    # pt 1
    print('++++++++++++       PART ONE        +++++++++++++')
    pairs_in_order = []
    for i in range(0, len(lines), 3):
        left = eval(lines[i])
        right = eval(lines[i+1])

        pair = i // 3 + 1
        print(f'\n== Pair {pair} ==')
        correct = in_correct_order(left, right, verbose=True) > 0
        print(f'Pairs {color.RED +"ARE NOT" if not correct else color.GREEN+"ARE"}{color.END} in the correct order')
        if correct:
            pairs_in_order.append(pair)

    print(f'\nPairs {pairs_in_order} were correct for a score of: {color.CYAN}{sum(pairs_in_order)}{color.END}')

    # pt 2
    print('\n++++++++++++       PART TWO        +++++++++++++')
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines() if not l == '\n']

    divider_1 = '[[2]]'
    divider_2 = '[[6]]'
    dividers = [divider_1, divider_2]
    lines += dividers
    lines = merge_sort_lines(lines)
    print('Sorted lists')
    print('\n'.join([f'{color.GREEN if l in dividers else ""}{i+1}. {l}{color.END if l in dividers else ""}'
                     for i, l in enumerate(lines)]))

    divider_idx_prod = 1
    for i, item in enumerate(lines):
        if item in dividers:
            divider_idx_prod *= i+1
    print(f'Decoder key {color.CYAN}{divider_idx_prod}{color.END}')



# testing
run_tests('distress_signal_test_input.txt')

# Actual work
run_tests('distress_signal_input.txt')


