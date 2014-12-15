__author__ = 'Ismius'
from random import randint
import time
from copy import deepcopy
import sys

board = []
ship_loc = []
ship_origin = [0 for x in range(4)]
for x in range(6):
    board.append(['O'] * 6)

ship_num = raw_input('How many ships would you like to place on the board?: ')
if int(ship_num) == 0:
    print 'Using default of 2'
    ship_num = 2
else:
    ship_num = int(ship_num)


def cls():
    print '\n' * 100


cls()


def print_board(board):
    print 'BATTLESHIP'
    k = 0
    disp_board = deepcopy(board)
    disp_board.insert(0, ['1', '2', '3', '4', '5', '6'])
    for row in disp_board:
        row.insert(0, str(k))
        k += 1
    for row in disp_board:
        print ' '.join(row)


print_board(board)


def place_ship(board, ship_loc=[]):  # returns list of coordinates that mean a hit
    invalid = 1
    place_count = 0
    while invalid:
        place_count += 1
        if place_count == 500:
            print'You tried putting too many ships on the board'
            sys.exit()
        ship_origin[0] = randint(0, len(board) - 1)  # row
        ship_origin[1] = randint(0, len(board[0]) - 1)  # column
        ship_origin[2] = randint(-1, 1)  # orientation row
        ship_origin[3] = randint(-1, 1)  # orientation column

        if ship_origin[2] == 0 and ship_origin[3] == 0:  # makes sure ship is 2 long
            continue

        new_ship_loc = [[ship_origin[0], ship_origin[1]],
                        [ship_origin[0] + ship_origin[2], ship_origin[1] + ship_origin[3]]]
        overlap = 0

        for new_coordinate in new_ship_loc:
            for old_coordinate in ship_loc:
                if new_coordinate == old_coordinate:
                    overlap = 1

        if (new_ship_loc[1][0] < 0 or new_ship_loc[1][0] > len(board) - 1) or (
                new_ship_loc[1][1] < 0 or new_ship_loc[1][1] > len(board[0]) - 1):
            continue
        elif overlap == 1:
            continue
        else:
            for coordinate_pair in new_ship_loc:
                ship_loc.append(coordinate_pair)
            invalid = 0


for x in range(ship_num):
    place_ship(board, ship_loc)

end = 0
while not end:
    hit = 0
    all_hit = 1
    time.sleep(2)
    cls()
    print_board(board)
    out_bounds = 1
    while out_bounds:
        shoot_str = raw_input('Coordinates to shoot at, sir?: ')
        shoot_str = shoot_str.translate(None, ', ')
        shoot = [int(shoot_str[0]) - 1, int(shoot_str[-1:]) - 1]

        if len(shoot_str) != 2:
            cls()
            print_board(board)
            print 'Those coordinates don\'t make sense sir'
        elif (shoot[0] < 0 or shoot[0] > len(board)) or (shoot[1] < 0 or shoot[1] > len(board[0])):
            cls()
            print_board(board)
            print'Those coordinates are out of range, sir.'
        else:
            out_bounds = 0


    for test_coordinate in ship_loc:
        if test_coordinate == shoot:
            board[shoot[0]][shoot[1]] = "X"  # changes board if hit
            cls()
            print_board(board)
            print "You got em' sir!"
            hit = 1
        if board[test_coordinate[0]][test_coordinate[1]] != 'X':  # test to see if every location has been hit
            all_hit = 0
    if hit == 0:
        board[shoot[0]][shoot[1]] = "~"
        cls()
        print_board(board)
        print "We've missed, sir."
    if all_hit == 1:
        cls()
        print_board(board)
        print "Congratulations! You have won!"
        misses = 0
        for row in board:
            for pos in row:
                if pos == '~':
                    misses += 1
        print 'Accuracy:', str(float(ship_num*2) / float(misses) * 100) + '%'
        end = 1

