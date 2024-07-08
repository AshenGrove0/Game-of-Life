import numpy as np
import pprint
import time
import copy
import sys
import argparse
import os
# use file reading to give examples of interesting starting coords to user 
# Chatgpt used to speed up the generation of starting coordinates to save me counting 0-indexed coordinates
# add an option for random noise start
"""
for row in colour_board:
            print("  ".join(row))
this is adapted from online
"""
def main():
    file, board_diamensions, display_type = parse_args()
    start()
    alive_coords_to_start = fetch_starting_coords(file)
    board = generate_starting_board(alive_coords_to_start,board_diamensions)
    run(board, board_diamensions, display_type)

def print_board(board):
    WHITE = "\u001b[33m#\u001b[0m"
    BLACK = "\u001b[31m#\u001b[0m"
    colour_board = copy.deepcopy(board)
    for row in range(len(board)):
        for column in range(len(board[row])):
            colour_board[row][column] = WHITE if board[row][column] == 1 else BLACK
    for row in colour_board:
        print("  ".join(row))

def parse_args():
    parser = argparse.ArgumentParser(
    prog="main.py",
    description="A numerical simulation of Conway's Game of Life",
    usage="python3 main.py [-h] [-f FILENAME] width height"
)
    parser.add_argument('width', help='width in squares of board')
    parser.add_argument('height', help='height in squares of board')
    parser.add_argument('-f', '--filename', help="path to file with starting coordinates, default is /coords.txt")
    parser.add_argument('-d', '--display', help="display type for board - `raw` or `colour`")

    args = parser.parse_args()
    print(args)
    board_diamensions = {
    'x': int(args.width),
    'y': int(args.height)
    }
    args.filename = "coords.txt" if args.filename == None else args.filename
    return args.filename, board_diamensions, args.display


def start():
    """Prints introduction to program"""
    coloured_name = "\u001b[32mConway's Game of Life\u001b[0m"
    BOLD = '\u001b[1m'
    GREEN = '\u001b[32m'
    RED = '\u001b[31m'
    YELLOW = '\u001b[33m'
    END = '\u001b[0m'
    print(f"""
          This is a simulation of {coloured_name}.

          Here are the rules, courtesy of Wikipedia:

            Any live cell with {BOLD}fewer than two{END} live neighbours {RED}dies{END}, as if by underpopulation.

            Any live cell with {BOLD}two or three{END} live neighbours {GREEN}lives on{END} to the next generation.

            Any live cell with {BOLD}more than three{END} live neighbours {RED}dies{END}, as if by overpopulation.

            Any dead cell with {BOLD}exactly three{END} live neighbours {YELLOW}becomes a live cell{END}, as if by reproduction.
          
          Input your starting coordinates in the file `coords.txt` in the format:
            X,Y
            A,B
          before running this program
          """)
    check_empty() # make sure this works with the presets
    time.sleep(3)
    os.system('clear')
        



def check_empty():
    with open('coords.txt', "r") as f:
        raw = f.readlines()
    for line in raw:
        if line != '':
            return False
    print("""
        \u001b[31mCause of crash: `coords.txt` is empty.\u001b[0m
              """)
    quit()


def fetch_starting_coords(file):
    with open(file, "r") as f:
        raw = f.readlines()
    coords = []
    for line in raw:
        coords.append(tuple(int(x) for x in line.strip(' ').split(',')))
    print(coords)
    return coords

def generate_starting_board(alive_coords_to_start: list, board_diamensions):
    '''Generates a board of provided size with alive cells at provided coordinates'''
    board = [[0 for i in range(board_diamensions['x'])] for i in range(board_diamensions['y'])]
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            if (row, column) in alive_coords_to_start:
                board[row][column] = 1
            else:
                board[row][column] = 0
    return board

def get_neighbour_count(board,row,column):
    '''Returns the number of adjacent alive cells to the cell with coordinates provided'''
    neighbour_count = 0
    for y in range(column-1, column+2):
        for x in range(row-1, row+2):
            try:
                if board[x][y] == 1:
                    neighbour_count += 1 
            except:
                pass # imagine all non existant cells are dead
    return neighbour_count 
    
def run(board: list, board_diamensions: dict, display_type: str):
    'Recursively runs one iteration of the game, checking to see if cells are alive and modifying itself accordingly'
    time.sleep(1)
    os.system('clear')
    board = list(board)
    print_board(board)
    
    new_board = copy.deepcopy(board)
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            neighbour_count = get_neighbour_count(board,row,column)
            #for live cells
            if board[row][column] == 1:
                neighbour_count -= 1
                if neighbour_count < 2 or neighbour_count > 3:
                    new_board[row][column] = 0
                elif neighbour_count == 2 or neighbour_count == 3:
                    new_board[row][column] = 1
            # for dead cells
            if board[row][column] == 0:
                if neighbour_count == 3:
                    new_board[row][column] = 1
        

    run(new_board, board_diamensions, display_type)





if __name__ == '__main__':
    main()