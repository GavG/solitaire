from textwrap import wrap
import timeit

def print_bitboard(board):
    board_string = '{:064b}'.format(board)[15:]
    print('\n'.join([' '.join(wrap(line, 1)) for line in wrap(board_string, 7)]))
    print('\n')

def str_to_bitboard(string):
    return int(''.join(string.split()), 2)

def is_valid_move(board, direction, position):
    if direction == 'up':
        move_board = ((1 << 14) ^ (1 << 7) ^ 1) << (position - 7)
        result = move_board ^ board
        return (result & move_board) == (1 << (position + 7)), result

    if direction == 'down':
        move_board = ((1 << 14) ^ (1 << 7) ^ 1) << (position - 7)
        result = move_board ^ board
        return (result & move_board) == (1 << (position - 7)), result

    if direction == 'right':
        move_board = 7 << (position - 1)
        result = move_board ^ board
        return (result & move_board) == (1 << position - 1), result

    if direction == 'left':
        move_board = 7 << (position - 1)
        result = move_board ^ board
        return (result & move_board) == (1 << position + 1), result

def solve(board, solution):
    if board in seen_boards:
        return
    else:
        seen_boards[board] = 1

    print_bitboard(board)

    #         46, 45, 44,
    #         39, 38, 37,
    # 34, 33, 32, 31, 30, 29, 28,
    # 27, 26, 25, 24, 23, 22, 21,
    # 20, 19, 18, 17, 16, 15, 14,
    #         11, 10, 9 ,
    #         4 , 3 , 2 ,

    for pos in [39, 38, 37, 32, 31, 30, 27, 26, 25, 24, 23, 22, 21, 18, 17, 16, 11, 10, 9]:
        solve_dir('up', pos, board, solution[:])
        solve_dir('down', pos, board, solution[:])

    for pos in [45, 38, 33, 32, 31, 30, 29, 26, 25, 24, 23, 22, 19, 18, 17, 16, 15, 10, 3]:
        solve_dir('left', pos, board, solution[:])
        solve_dir('right', pos, board, solution[:])


def solve_dir(direction, pos, board, solution):
    valid, result = is_valid_move(board, direction, pos)
    if valid:
        solution.append((direction, pos))
        if (result == board_target):
            print('SOLUTION FOUND!\n')
            print_bitboard(result)
            print(solution)
            print('\nTime taken: ')
            print(timeit.default_timer() - start_time)
            exit()
        else:
            solve(result, solution)

def main():
    setup()
    print('Solving...\n')
    global start_time
    start_time = timeit.default_timer()
    solve(board, [])

def setup():
    global board_target
    global board_string
    global board
    global board_len
    global seen_boards

    board_target = str_to_bitboard("""
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

    board = str_to_bitboard(board_string)
    board_len = len(''.join(board_string.split()))
    seen_boards = {}

if __name__ == "__main__":
    main()
