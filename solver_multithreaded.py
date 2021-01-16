from textwrap import wrap
import threading
from queue import Queue
from pprint import pprint
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
    global seen_boards

    if board in seen_boards:
        return
    else:
        seen_boards[board] = 1

    # print_bitboard(board)

    #         46, 45, 44,
    #         39, 38, 37,
    # 34, 33, 32, 31, 30, 29, 28,
    # 27, 26, 25, 24, 23, 22, 21,
    # 20, 19, 18, 17, 16, 15, 14,
    #         11, 10, 9 ,
    #         4 , 3 , 2 ,

    for pos in [39, 38, 37, 32, 31, 30, 27, 26, 25, 24, 23, 22, 21, 18, 17, 16, 11, 10, 9]:
        job_queue.put({'direction': 'up', 'pos': pos,
                       'board': board, 'solution': solution[:]})
        job_queue.put({'direction': 'down', 'pos': pos,
                       'board': board, 'solution': solution[:]})

    for pos in [45, 38, 33, 32, 31, 30, 29, 26, 25, 24, 23, 22, 19, 18, 17, 16, 15, 10, 3]:
        job_queue.put({'direction': 'left', 'pos': pos,
                       'board': board, 'solution': solution[:]})
        job_queue.put({'direction': 'right', 'pos': pos,
                       'board': board, 'solution': solution[:]})

def solve_dir(direction, pos, board, solution):
    global running
    valid, result = is_valid_move(board, direction, pos)
    if valid:
        solution.append((direction, pos))
        if (result == board_target):
            running = False
            print('SOLUTION FOUND!\n')
            print_bitboard(result)
            pprint(solution)
            print(timeit.default_timer() - start_time)
            exit()
        else:
            solve(result, solution)

def process_queue(job_queue):
    global running
    while running:
        args = job_queue.get()
        solve_dir(**args)
        job_queue.task_done()

def main():
    setup()
    global start_time
    start_time = timeit.default_timer()
    print('Solving...\n')
    solve(board, [])

    for i in range(no_threads):
        worker = threading.Thread(target=process_queue, args=(job_queue,), daemon = True)
        worker.start()

    job_queue.join()

def setup():
    global running
    global no_threads

    global board_target
    global board_string
    global board
    global board_len
    global seen_boards
    global job_queue

    running = True
    no_threads = 10

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
    job_queue = Queue()

if __name__ == "__main__":
    main()
