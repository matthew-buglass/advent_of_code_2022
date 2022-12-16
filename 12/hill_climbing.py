"""
Problem Notes:
    - a lowest elevation, z highest.
    - S = current position
    - E = best signal
    - S = a
    - E = z
    - Take as few steps as possible
        - one step cardinal
        - only go up one elevation at a time
"""


def get_idx(row, col, puzzle_input):
    if row < 0 or col < 0:
        return None

    try:
        return puzzle_input[row][col]
    except IndexError:
        return None


class Step:
    def __init__(self, row, col, current_steps, max_step_up, height_symbol, parent, src_direction, trail_head=None):
        self.row: int = row
        self.col: int = col
        self.current_steps: int = current_steps
        self.max_step_up: int = max_step_up
        self.height: str = height_symbol
        self.trail_head: Step = trail_head if trail_head else self

        if self.height == 'S':
            self.height_val: int = 0
        elif self.height == 'E':
            self.height_val: int = 25
        else:
            self.height_val = ord(self.height) - 97

        self.parent: Step = parent
        self.orientation_from_parent: str = src_direction

        self.top: Step = None
        self.bot: Step = None
        self.right: Step = None
        self.left: Step = None

    def __str__(self):
        return f'Location ({self.row}, {self.col}), Symbol {self.height}, Steps {self.current_steps}'

    def __eq__(self, other):
        if other is None:
            return False
        return self.row == other.row and self.col == other.col

    def is_trailhead(self):
        return self == self.trail_head

    def make_children(self, puzzle_input):
        self.bot = None if not get_idx(self.row+1, self.col, puzzle_input) else \
            Step(
                row=self.row + 1,
                col=self.col,
                current_steps=self.current_steps + 1,
                max_step_up=self.max_step_up,
                height_symbol=get_idx(self.row + 1, self.col, puzzle_input),
                parent=self,
                src_direction='v',
                trail_head=self.trail_head
            )
        self.top = None if not get_idx(self.row - 1, self.col, puzzle_input) else \
            Step(
                row=self.row - 1,
                col=self.col,
                current_steps=self.current_steps + 1,
                max_step_up=self.max_step_up,
                height_symbol=get_idx(self.row - 1, self.col, puzzle_input),
                parent=self,
                src_direction='^',
                trail_head=self.trail_head
            )
        self.right = None if not get_idx(self.row, self.col + 1, puzzle_input) else \
            Step(
                row=self.row,
                col=self.col + 1,
                current_steps=self.current_steps + 1,
                max_step_up=self.max_step_up,
                height_symbol=get_idx(self.row, self.col + 1, puzzle_input),
                parent=self,
                src_direction='>',
                trail_head=self.trail_head
            )
        self.left = None if not get_idx(self.row, self.col - 1, puzzle_input) else \
            Step(
                row=self.row,
                col=self.col - 1,
                current_steps=self.current_steps + 1,
                max_step_up=self.max_step_up,
                height_symbol=get_idx(self.row, self.col - 1, puzzle_input),
                parent=self,
                src_direction='<',
                trail_head=self.trail_head
            )

    def get_reachable_children(self):
        if self.at_apex():
            return []
        elif self.is_trailhead() and self.current_steps > 0:
            return []
        else:
            return [
                c for c in [self.top, self.bot, self.right, self.left] if
                c and c.height_val - self.height_val <= self.max_step_up
            ]
    
    def at_apex(self):
        return self.height == 'E'
    
    def at_start(self):
        return self.is_trailhead()

    def is_start(self):
        return self.height == 'S' and self.current_steps == 0
    
    def at_start_or_end(self):
        return self.at_start() or self.at_apex()


class Path:
    def __init__(self, puzzle_arr, trail_head_location, max_steps_up, steps_to_beat=-1):
        self.puzzle: list[list[str]] = puzzle_arr
        self.trail_head: Step = Step(
            row=trail_head_location[0],
            col=trail_head_location[1],
            current_steps=0,
            max_step_up=max_steps_up,
            height_symbol=get_idx(trail_head_location[0], trail_head_location[1], self.puzzle),
            parent=None,
            src_direction='',
        )
        self.trail_tails: list[Step] = [self.trail_head]
        self.best_path_tail: Step = self.trail_head
        self.visited_steps: list[Step] = []
        self.steps_to_beat = steps_to_beat

    def _get_best_and_add_next_steps(self):
        current_best = self.trail_tails.pop(0)
        current_best.make_children(self.puzzle)
        children = current_best.get_reachable_children()
        new_steps = [c for c in children if c not in self.visited_steps]
        self.trail_tails += new_steps
        self.visited_steps += new_steps
        self.trail_tails.sort(key=lambda x: x.current_steps)

        return current_best

    def _found_end(self):
        try:
            return self.trail_tails[0].at_apex()
        except IndexError:
            return False

    def best_path_string(self):
        num_rows, num_cols = len(self.puzzle), len(self.puzzle[0])
        path_arr = [['.' for _ in range(num_cols)] for _ in range(num_rows)]

        curr_tail = self.best_path_tail
        path_arr[curr_tail.row][curr_tail.col] = curr_tail.height
        while curr_tail.parent is not None:
            curr_parent = curr_tail.parent
            path_arr[curr_parent.row][curr_parent.col] = curr_tail.orientation_from_parent
            curr_tail = curr_parent

        return '\n'.join([''.join(r) for r in path_arr])

    def is_still_candidate(self):
        return self.steps_to_beat < 0 or self.best_path_tail.current_steps < self.steps_to_beat

    def find_path(self, verbosity=0):
        while not self._found_end() and len(self.trail_tails) > 0 and self.is_still_candidate():
            curr_best = self._get_best_and_add_next_steps()
            self.best_path_tail = curr_best

            if verbosity >= 2:
                print(f'Current best path:\n\t{curr_best}')

        try:
            self.best_path_tail = self.trail_tails[0]
        except IndexError:
            pass

        self.print_summary(verbosity >= 1)

    def print_summary(self, print_trail=False):
        if self.best_path_tail.at_apex():
            print(f'Best path tail:'
                  f'\n\tStarting at: {self.trail_head}'
                  f'\n\tEnding at: {self.best_path_tail}')
        elif len(self.trail_tails) == 0:
            print(f'Hit dead end:'
                  f'\n\tStarting at: {self.trail_head}'
                  f'\n\tEnding at: {self.best_path_tail}')
        else:
            print(f"Stopped short, because couldn't beat current best of {self.steps_to_beat}:"
                  f'\n\tStarting at: {self.trail_head}'
                  f'\n\tEnding at: {self.best_path_tail}')

        if print_trail:
            print(f'{self.best_path_string()}\n')


def run_tests(filename, verbosity):
    with open(filename, "r") as f:
        puzzle_arr = [list(l.strip()) for l in f.readlines()]

    print('\n=======    Part 1   ========')
    start_location = (0, 0)
    for i, row_val in enumerate(puzzle_arr):
        for j, col_val in enumerate(row_val):
            if col_val == 'S':
                start_location = (i, j)
                break

    path = Path(puzzle_arr, trail_head_location=start_location, max_steps_up=1)
    path.find_path(verbosity=verbosity)

    print('\n=======    Part 2   ========')
    best_result: Path = None
    best_steps = -1
    for i, row_val in enumerate(puzzle_arr):
        for j, col_val in enumerate(row_val):
            if col_val == 'S' or col_val == 'a':
                path = Path(puzzle_arr, trail_head_location=(i, j), max_steps_up=1, steps_to_beat=best_steps)
                path.find_path(verbosity=verbosity)
                if not best_result or \
                        best_result.best_path_tail.current_steps > path.best_path_tail.current_steps and \
                        path.best_path_tail.at_apex():
                    best_result = path
                    best_steps = best_result.best_path_tail.current_steps

    best_result.print_summary(verbosity+1)


# testing
run_tests('hill_climbing_test_input.txt', 1)

# Actual work
run_tests('hill_climbing_input.txt', 0)
