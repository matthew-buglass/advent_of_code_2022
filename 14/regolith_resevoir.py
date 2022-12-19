'''
Problem Notes
'''

from pandas import DataFrame as df


def get_positions_in_line_set(start: list[int, int], end: list[int, int]):
    if start[0] == end[0]:
        return {(start[0], c) for c in range(start[1], end[1])}
    else:
        return {(r, start[1]) for r in range(start[0], end[0])}


class RockFormation:
    def __init__(self, puzzle_input: str):
        self.locations = set()
        self.min_x = 100000000
        self.max_x = 0
        self.max_y = 0

        traces: list[str] = [location for location in puzzle_input.split(' -> ')]

        for i in range(len(traces)-1):
            start, end = [int(l) for l in traces[i]], [int(l) for l in traces[i+1]]
            self.locations.union(get_positions_in_line_set(start, end))


class RockFace:
    def __init__(self, puzzle_lines: list[str], sand_start: tuple[int, int]):
        self.rock_formations = [RockFormation(s) for s in puzzle_lines]
        self.min_x = min([r.min_x] for r in self.rock_formations)
        self.max_x = min([r.max_x] for r in self.rock_formations)
        self.max_y = min([r.max_y] for r in self.rock_formations)

        self.sand_start = sand_start
        self.sand_locations = {}

    def __str__(self):
        rock_sym = '#'
        air_sym = '.'




def run_tests(filename):
    with open(filename, 'r') as f:
        pass


# testing
run_tests('regolith_resevoir_test_input.txt')

# Actual work
# run_tests('regolith_resevoir_input.txt')


