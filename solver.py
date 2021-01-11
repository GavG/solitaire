from textwrap import wrap

def print_bitboard(board):
    board_string = '{:064b}'.format(board)[15:]
    print('\n'.join([' '.join(wrap(line, 1)) for line in wrap(board_string, 7)]))
    print('\n')

def str_to_bitboard(string):
    return int(''.join(string.split()), 2)

def is_valid_move(board, direction, position):
    if direction == 'y':
        move_board = ((1 << 14) ^ (1 << 7) ^ 1) << position
        result = move_board ^ board
        return (result & move_board) == (1 << (14 + position)), result

    if direction == 'right':
        move_board = 7 << (position - 1) # 7 = '111'
        result = move_board ^ board
        return (result & move_board) == (1 << position - 1), result

    if direction == 'left':
        move_board = 7 << (position - 1)  # 7 = '111'
        result = move_board ^ board
        return (result & move_board) == (1 << position + 1), result

board_mask = str_to_bitboard("""
1100011
1100011
0000000
0000000
0000000
1100011
1100011
""")

board = str_to_bitboard("""
1111111
1111111
1111111
1110111
1111111
1111111
1111111
""")

# valid, result = is_valid_move(board, 'y', 10)
# print('y')
# print(valid)
# print_bitboard(result)

valid, result = is_valid_move(board, 'right', 25)
print('right')
print(valid)
print_bitboard(result)

valid, result = is_valid_move(board, 'left', 23)
print('left')
print(valid)
print_bitboard(result)
