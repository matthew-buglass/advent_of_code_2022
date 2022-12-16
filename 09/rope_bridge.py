"""
Notes:
    - H and T always touching (euclid dist <= 1)
        - Same row OR col move horiz/vert
        - Diff row AND col move diag
    - Both start overlapping
    - Input: <direction> <num_moves>
    - Start pos (s): Undefined
    - Count places tail visited at least once
    - Pt: 1 count number visited

Design:
    - Set of coordinates
        - arr[<row>][<col>]
        - Entities:
            - Head: H
            - Tail: T
            - Start: s
            - Tail visited: Bool
    - Determine array size based on input moves and infer starting point
"""


def move_piece(piece_pos, parent_post):
    row_dist = parent_post[0] - piece_pos[0]
    col_dist = parent_post[1] - piece_pos[1]

    new_row = piece_pos[0] - 1 if row_dist < 0 else piece_pos[0] + 1
    new_col = piece_pos[1] - 1 if col_dist < 0 else piece_pos[1] + 1

    # Head and tail are touching = do nothing
    if abs(row_dist) < 2 and abs(col_dist) < 2:
        return piece_pos
    # same col, diff row = shift row
    elif abs(row_dist) == 2 and abs(col_dist) == 0:
        return new_row, piece_pos[1]
    # same row, diff col = shift col
    elif abs(row_dist) == 0 and abs(col_dist) == 2:
        return piece_pos[0], new_col
    # Otherwise move diagonally
    else:
        return new_row, new_col


class Move:
    def __init__(self, move_str):
        direction, dist = move_str.split()
        self.axis = 'r' if direction in ['L', 'R'] else 'c'
        self.distance = int(dist) if direction in ['R', 'D'] else -int(dist)
        self.name = move_str

    def details(self):
        return self.axis, self.distance


class RopeSimulation:
    def __init__(self, move_list, num_knots=2):
        self.moves = [Move(m) for m in move_list]
        self.width, self.height, self.start = self._infer_board_size_and_start()
        self.head = self.start
        self.tail = self.start
        self.visited = {self.start}
        self.knots = [self.start for _ in range(num_knots-2)]

        self.move_history = [self.string_with_header('Initial State')]
    
    def reset(self):
        self.head = self.start
        self.tail = self.start
        self.visited = {self.start}

        self.move_history = [self.string_with_header('Initial State')]

    def __str__(self):
        return '\n'.join([''.join(r) for r in self._str_lists()])

    def _str_lists(self):
        str_arr = [['.' for _ in range(self.width)] for _ in range(self.height)]
        str_arr[self.start[0]][self.start[1]] = 's'
        str_arr[self.tail[0]][self.tail[1]] = 'T'

        if self.knots:
            knots_rev = list(range(0, len(self.knots)))
            knots_rev.reverse()
            for knot_num in knots_rev:
                pos = self.knots[knot_num]
                str_arr[pos[0]][pos[1]] = str(knot_num + 1)

        str_arr[self.head[0]][self.head[1]] = 'H'

        if self.head == self.tail or self.head == self.start:
            msg = '   (H covers{}{}{})'.format(
                ' T' if self.head == self.tail else '',
                ',' if self.head == self.tail == self.start else '',
                ' s' if self.head == self.start else '')
            str_arr[-1].append(msg)
            for i in range(len(str_arr)-1):
                str_arr[i].append(' ' * len(msg))

        return str_arr

    def string_with_header(self, header):
        return "{eq} {h} {eq}\n{s}".format(eq='='*5, h=header, s=str(self))

    def tail_travel_string(self):
        str_arr = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for location in self.visited:
            str_arr[location[0]][location[1]] = '#'

        str_arr[self.start[0]][self.start[1]] = 's'
        string_combined = '\n'.join([''.join(r) for r in str_arr])
        return "{eq} {h} {eq}\n{s}".format(eq='='*5, h="Tailiver's Travels", s=string_combined)

    def _infer_board_size_and_start(self):
        # pos = (curr, min, max)
        x_pos = (0, 0, 0)
        y_pos = (0, 0, 0)

        for move in self.moves:
            axis, dist = move.details()
            if axis == 'r':
                new_x_pos = x_pos[0] + dist
                x_pos = (new_x_pos, min(new_x_pos, x_pos[1]), max(new_x_pos, x_pos[2]))
            else:
                new_y_pos = y_pos[0] + dist
                y_pos = (new_y_pos, min(new_y_pos, y_pos[1]), max(new_y_pos, y_pos[2]))

        # normalize values
        width = abs(x_pos[1]) + x_pos[2] + 1
        height = abs(y_pos[1]) + y_pos[2] + 1
        start = (abs(y_pos[1]), abs(x_pos[1]))

        return width, height, start

    def _move_head(self, axis, dist):
        if axis == 'r':
            self.head = (self.head[0], self.head[1] + dist)
        else:
            self.head = (self.head[0] + dist, self.head[1])

    def _adjust_tail(self):
        parent = self.head

        for i in range(len(self.knots)):
            self.knots[i] = move_piece(self.knots[i], parent)
            parent = self.knots[i]

        self.tail = move_piece(self.tail, parent)

        self.visited.add(self.tail)

    def make_move(self, move, verbosity=0):
        axis, dist = move.details()
        dist_is_negative = dist < 0

        for i in range(abs(dist)):
            self._move_head(axis, -1) if dist_is_negative else self._move_head(axis, 1)
            self._adjust_tail()

            if verbosity > 1:
                state = self.string_with_header(move.name) if i == 0 else str(self)
                self.move_history.append(state)
                print("\n{}".format(state))

        if verbosity == 1:
            state = self.string_with_header(move.name)
            self.move_history.append(state)
            print("\n{}".format(state))
    
    def run_all_moves(self, verbosity=0):
        for move in self.moves:
            self.make_move(move, verbosity)

        state = self.string_with_header('Final State')
        self.move_history.append(state)
        if verbosity > 0:
            print("\n{}".format(state))

    def run_all_moves_progress_only(self):
        num_moves = len(self.moves)
        for i in range(num_moves):
            self.make_move(self.moves[i], 0)
            if i % 100 == 0:
                print(f'Ran {i:,} moves out of {num_moves:,}')


# testing
with open('rope_bridge_test_input.txt', 'r') as f:
    moves = [i.strip() for i in f.readlines()]

sim = RopeSimulation(moves)
print()
sim.run_all_moves(2)
print()
print('\n\n'.join(sim.move_history))
print(sim.tail_travel_string())
print(f'Number of place the tail visited with no knots {len(sim.visited)}')

sim.reset()

with open('rope_bridge_test_input_2.txt', 'r') as f:
    moves = [i.strip() for i in f.readlines()]
print()
sim_knots = RopeSimulation(moves, num_knots=10)
print()
sim_knots.run_all_moves(1)
print()
print('\n\n'.join(sim_knots.move_history))
print(sim_knots.tail_travel_string())
print(f'Number of place the tail visited with many knots {len(sim_knots.visited)}')


# Actual work
with open('rope_bridge_input.txt', 'r') as f:
    moves = [i.strip() for i in f.readlines()]

print()
real_sim = RopeSimulation(moves, num_knots=10)
print()
real_sim.run_all_moves_progress_only()
print(real_sim.tail_travel_string())
print(f'Number of place the tail visited with two knots {len(real_sim.visited)}')

real_sim.reset()


