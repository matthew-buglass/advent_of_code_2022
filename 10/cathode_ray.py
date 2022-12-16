"""
addx V:
    - 2 cycles
    - adds V to register
noop:
    - 1 cycle
    - does nothing
"""
screen_width = 40
lit = '#'
dark = '.'
dark_screen = dark * screen_width


def during_cycle_pt_1(stop_pts, register_v, cycle_num):
    if cycle_num in stop_pts:
        print('Register has value {} during cycle {}\nAdditional signal strength {}'.format(
            register_v,
            cycle_num,
            register_v * cycle_num
        ))
        return register_v * cycle_num
    return 0


def during_cycle_pt_2(sprint_pos, current_row):
    drawn_col = len(current_row)
    sprite_range = list(range(sprint_pos - 1, sprint_pos + 2))

    if drawn_col in sprite_range:
        current_row += lit
    else:
        current_row += dark

    lead_dark_len = max(0, sprite_range[0])
    sprite_len = sum([1 for p in sprite_range if 0 <= p < 40])
    tail_dark_len = max(0, 39-sprite_range[-1])

    print(f'Sprite position {sprint_pos}\n'
          f'Drawing pixel {drawn_col}\n'
          f'Current row:    {current_row}\n'
          f'Pixel position: {dark*lead_dark_len}{lit*sprite_len}{dark*tail_dark_len}\n')

    return current_row


def run_test(filename):
    with open(filename, 'r') as f:
        instructions = [l.strip().split() for l in f]

    register_val = 1
    cycle = 0
    total_sig_strength = 0
    stop_points = [20, 60, 100, 140, 180, 220]
    crt_rows = []
    curr_row_str = ''

    for i in instructions:
        # start first cycle
        cycle += 1

        # during first cycle
        # total_sig_strength += during_cycle_pt_1(stop_points, register_val, cycle)
        curr_row_str = during_cycle_pt_2(register_val, curr_row_str)

        # end first cycle
        if cycle % 40 == 0:
            crt_rows.append(curr_row_str)
            curr_row_str = ''
        # addx second cycle
        if len(i) != 1:
            # start second cycle
            cycle += 1

            # during second cycle
            # total_sig_strength += during_cycle_pt_1(stop_points, register_val, cycle)
            curr_row_str = during_cycle_pt_2(register_val, curr_row_str)

            # end second cycle
            register_val += int(i[-1])
            if cycle % 40 == 0:
                crt_rows.append(curr_row_str)
                curr_row_str = ''

    # print('Total test signal strength for points {}: {}'.format(stop_points, total_sig_strength))
    print('Resultant CRT:\n{}'.format("\n".join(crt_rows)))


# testing
run_test('cathode_ray_test_input.txt')

# Actual work
print()
run_test('cathode_ray_input.txt')
