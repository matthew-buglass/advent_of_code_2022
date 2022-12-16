# start packet = 4 different chars
# input: stream buffer track 4 most recent to be diff for start message
# Position = # chars from start to end of start indicator

def all_diff(chars_list: str):
    char_set = set(chars_list)
    return len(char_set) == len(chars_list)


with open('tuning_input.txt', 'r') as f:
    pos = 4
    chars = [f.read(1) for _ in range(pos)]

    while not all_diff(chars):
        chars = chars[1:]
        chars.append(f.read(1))
        pos += 1

    print('Packet start position: {}'.format(pos))


with open('tuning_input.txt', 'r') as f:
    pos = 14
    chars = [f.read(1) for _ in range(pos)]

    while not all_diff(chars):
        chars = chars[1:]
        chars.append(f.read(1))
        pos += 1

    print('Message start position: {}'.format(pos))
