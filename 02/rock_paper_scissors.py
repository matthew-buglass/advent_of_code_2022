
def win_loss_draw_score(match, wins, losses):
    if match in wins:
        return 6
    elif match in losses:
        return 0
    else:
        return 3


def get_match_points(match, selection_points, wins, losses):
    return win_loss_draw_score(match, wins, losses) + selection_points[match[-1]]


with open('encrypted_rps.txt') as f:
    matches = [m.strip('\n') for m in f.readlines()]

    # Pt 1
    wins = ["A Y", "B Z", "C X"]
    losses = ["A Z", "B X", "C Y"]

    select_points = {
        'X': 1,
        'Y': 2,
        'Z': 3
    }

    scores = [get_match_points(m, select_points, wins, losses) for m in matches]
    print('Vanilla score: {}'.format(sum(scores)))

    # Pt 2
    opponent = "ABC"
    result = "XYZ"

    select_points = {
        'R': 1,
        'P': 2,
        'S': 3
    }
    result_points = {
        'X': 0,
        'Y': 3,
        'Z': 6
    }

    # loss, draw, win
    shapes = [
        ['S', 'R', 'P'],
        ['R', 'P', 'S'],
        ['P', 'S', 'R'],
    ]

    scores = [result_points[m[-1]] + select_points[shapes[opponent.find(m[0])][result.find(m[-1])]] for m in matches]
    print('Modified score: {}'.format(sum(scores)))

