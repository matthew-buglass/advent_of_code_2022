'''
Problem Notes
'''
import os
import time

from pandas import DataFrame as df

from const import flatten, color, clear_terminal


def get_positions_in_line(start: tuple[int, int], end: tuple[int, int]):
    if start[0] == end[0]:
        min_col = min(start[1], end[1])
        max_col = max(start[1], end[1])
        return [(start[0], c) for c in range(min_col, max_col + 1)]
    else:
        min_row = min(start[0], end[0])
        max_row = max(start[0], end[0])
        return [(r, start[1]) for r in range(min_row, max_row + 1)]


class RockFormation:
    def __init__(self, puzzle_input: str):
        self.locations = []
        self.min_col = 100000000
        self.max_col = 0
        self.max_row = 0

        traces: list[str] = [location for location in puzzle_input.split(' -> ')]

        for i in range(len(traces)-1):
            start = [int(co_ord) for co_ord in traces[i].split(',')]
            end = [int(co_ord) for co_ord in traces[i+1].split(',')]
            self.locations += get_positions_in_line(
                # Reversing input rows and columns so that they will index correctly
                (start[1], start[0]),
                (end[1], end[0])
            )

            self.min_col = min(self.min_col, start[0], end[0])
            self.max_col = max(self.max_col, start[0], end[0])
            self.max_row = max(self.max_row, start[1], end[1])

    def get_normalized_coordinates(self, min_col):
        return [(r, c - min_col) for r, c in self.locations]


class RockFace:
    def __init__(self, puzzle_lines: list[str], sand_start: tuple[int, int]):
        self.rock_formations = [RockFormation(s) for s in puzzle_lines]
        self.min_col = min([r.min_col for r in self.rock_formations])
        self.max_col = max([r.max_col for r in self.rock_formations])
        self.max_row = max([r.max_row for r in self.rock_formations])
        self.col_labels = [str(_) for _ in range(self.min_col, self.max_col + 1)]

        self.sand_start = (sand_start[1], sand_start[0])
        self.sand_locations = set()

        self.rock_locations = set(flatten([
            form.locations for form in self.rock_formations
        ]))
        self.normalized_rock_locations = set(flatten([
            form.get_normalized_coordinates(self.min_col) for form in self.rock_formations
        ]))

    def __str__(self):
        rock_sym = '#'
        air_sym = '.'
        sand_start_sym = '+'
        sand_sym = 'o'

        norm_sand_start_row, norm_sand_start_col = self.sand_start[0], self.sand_start[1] - self.min_col

        num_rows, num_cols = self.max_row + 1, self.max_col - self.min_col + 1

        current_formation = [[air_sym for _ in range(num_cols)] for _ in range(num_rows)]

        for x, y in self.normalized_rock_locations:
            current_formation[x][y] = rock_sym

        for x, y in self.get_normalized_sand_coordinates():
            current_formation[x][y] = sand_sym

        current_formation[norm_sand_start_row][norm_sand_start_col] = sand_start_sym

        data_frame = df(current_formation)
        return data_frame.to_string(header=self.col_labels)

    def get_normalized_sand_coordinates(self):
        return [(r, c - self.min_col) for r, c in self.sand_locations]

    def _print_mid_fall(self, sand_location, tail_text=""):
        self.sand_locations.add(sand_location)
        self_str = str(self) + "\n{}".format(tail_text)
        self.sand_locations.remove(sand_location)

        clear_terminal()
        print(self_str)

    def _get_next_sand_position(self, position: tuple[int, int]):
        down = (position[0] + 1, position[1])
        down_left = (position[0] + 1, position[1] - 1)
        down_right = (position[0] + 1, position[1] + 1)

        all_taken_locations = self.sand_locations | self.rock_locations

        if down not in all_taken_locations:
            return down
        elif down_left not in all_taken_locations:
            return down_left
        elif down_right not in all_taken_locations:
            return down_right
        else:
            return position

    def _run_one_sand_fall(self, verbose=False, extra_text=""):
        sand_curr_location = self.sand_start
        sand_last_location = (0, 0)

        while sand_curr_location != sand_last_location:
            sand_last_location = sand_curr_location
            sand_curr_location = self._get_next_sand_position(sand_curr_location)
            if verbose:
                self._print_mid_fall(sand_curr_location, extra_text)
                # time.sleep(0)

        self.sand_locations.add(sand_curr_location)

    def simulate_sand(self, number_of_grains):
        for _ in range(number_of_grains):
            self._run_one_sand_fall(True)

    def run_until_off_map(self, verbose=False):
        grains_in_map = 0

        while True:
            try:
                self._run_one_sand_fall(verbose, "Grain {}".format(grains_in_map + 1))
                grains_in_map += 1
            except IndexError:
                print(f"{color.CYAN}{grains_in_map}{color.END} grains of sand were able to come to rest")
                break


def run_tests(filename):
    with open(filename, 'r') as f:
        rock_wall = RockFace(
            puzzle_lines=[l.strip() for l in f.readlines()],
            sand_start=(500, 0)
        )

    # pt 1.
    rock_wall.run_until_off_map(True)


    # pt. 2


# testing
# run_tests('regolith_resevoir_test_input.txt')

# Actual work
run_tests('regolith_resevoir_input.txt')


