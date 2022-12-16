def get_row_vals(arr, row_idx):
    return arr[row_idx]


def get_col_vals(arr, col_idx):
    return [row[col_idx] for row in arr]


def calc_scenic_score_for_direction(tree_height, tree_list):
    score = 0

    for tree in tree_list:
        if tree < tree_height:
            score += 1
        else:
            score += 1
            break

    return score


def calc_scenic_score(tree_height, left, right, top, bottom):
    left.reverse()
    top.reverse()

    left_score = calc_scenic_score_for_direction(tree_height, left)
    right_score = calc_scenic_score_for_direction(tree_height, right)
    top_score = calc_scenic_score_for_direction(tree_height, top)
    bottom_score = calc_scenic_score_for_direction(tree_height, bottom)

    return left_score * right_score * top_score * bottom_score


def count_visible_trees(tree_arr):
    visible_trees = 0
    num_rows = len(tree_arr)
    num_cols = len(tree_arr[0])

    # all outer trees are visible
    num_outer_trees = num_rows * 2 + (num_cols - 2) * 2
    visible_trees += num_outer_trees

    # look at the interior trees
    for row_i in range(1, num_rows-1):
        for col_i in range(1, num_cols-1):
            tree_height = tree_arr[row_i][col_i]
            row_heights = get_row_vals(tree_arr, row_i)
            col_heights = get_col_vals(tree_arr, col_i)

            trees_left = row_heights[0:col_i]
            trees_right = row_heights[col_i+1:]
            trees_top = col_heights[0:row_i]
            trees_bottom = col_heights[row_i+1:]

            vis_left = tree_height > max(trees_left)
            vis_right = tree_height > max(trees_right)
            vis_top = tree_height > max(trees_top)
            vis_bottom = tree_height > max(trees_bottom)

            visible_trees += int(vis_left or vis_right or vis_top or vis_bottom)

    return visible_trees


def find_max_scenic_score(tree_arr):
    num_rows = len(tree_arr)
    num_cols = len(tree_arr[0])

    max_scenic_score = 0
    best_tree_location = (0, 0)
    best_tree_height = 0

    # look at each tree
    for row_i in range(num_rows):
        for col_i in range(num_cols):
            tree_height = tree_arr[row_i][col_i]
            row_heights = get_row_vals(tree_arr, row_i)
            col_heights = get_col_vals(tree_arr, col_i)

            trees_left = row_heights[0:col_i]
            trees_right = row_heights[col_i + 1:]
            trees_top = col_heights[0:row_i]
            trees_bottom = col_heights[row_i + 1:]

            scenic_score = calc_scenic_score(tree_height, trees_left, trees_right, trees_top, trees_bottom)

            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score
                best_tree_height = tree_height
                best_tree_location = (row_i, col_i)

    return max_scenic_score, best_tree_location, best_tree_height


# Testing
with open('tree_house_test_input.txt', 'r') as f:
    trees = [[int(t) for t in list(row.strip())] for row in f.readlines()]

print('Number of visible trees: {}\n'.format(count_visible_trees(trees)))
max_scenic_score, best_tree_location, best_tree_height = find_max_scenic_score(trees)
print('Tree in position: {}\nHas height: {}\nWith the Max scenic score of {}\n'.format(
    best_tree_location,
    best_tree_height,
    max_scenic_score
))


with open('tree_house_input.txt', 'r') as f:
    trees = [[int(t) for t in list(row.strip())] for row in f.readlines()]

# Pt 1
print('Number of visible trees: {}\n'.format(count_visible_trees(trees)))

# Pt 2
max_scenic_score, best_tree_location, best_tree_height = find_max_scenic_score(trees)
print('Tree in position: {}\nHas height: {}\nWith the Max scenic score of {}\n'.format(
    best_tree_location,
    best_tree_height,
    max_scenic_score
))

