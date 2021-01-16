import solver

board_mask = solver.str_to_bitboard("""
1100011
1100011
0000000
0000000
0000000
1100011
1100011
""")

board_target = solver.str_to_bitboard("""
1100011
1100011
0000000
0001000
0000000
1100011
1100011
""")

board_string = """
1111111
1111111
1111111
1110111
1111111
1111111
1111111
"""

board = solver.str_to_bitboard(board_string)
board_len = len(''.join(board_string.split()))
seen_boards = {}

print('Running tests')
valid_up, result = solver.is_valid_move(board, 'up', 17)
valid_down, result = solver.is_valid_move(board, 'down', 31)
valid_right, result = solver.is_valid_move(board, 'right', 25)
valid_left, result = solver.is_valid_move(board, 'left', 23)

if (valid_up and valid_down and valid_right and valid_left):
    print('All tests passed')
else:
    print("Tests failed")
    exit()
