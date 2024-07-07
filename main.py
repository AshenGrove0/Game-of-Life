import numpy as np
import pprint
import time
import copy
import pygame # or should be tkinter or something else? hack it w pillow and weird screencapture colour stuff?
# use file reading to give examples of interesting starting coords to user 
import tkinter as tk
import sys
# add an option for random noise start
board_diamensions = {
    'x': 8,
    'y': 10
}

alive_coords_to_start = [(3,2),(3,3),(3,4),(3,5)]

def main():
    if len(sys.argv) != 5:
        print("Usage: python main.py COORDS_FILE_NAME WIDTH HEIGHT") # you get your starting coords from a file
        sys.exit(1)
    coords_file_path = sys.argv[1]
    print('xwq')
    alive_coords_to_start = read_coords_file(coords_file_path)
    board_diamensions['x'] = int(sys.argv[2])
    board_diamensions['y'] = int(sys.argv[3])
    board = generate_starting_board(board_diamensions, alive_coords_to_start)
    pprint.pp(board)
    run(board,board_diamensions)

def generate_starting_board(board_diamensions, alive_coords_to_start):
    '''Generates a board of provided size with alive cells at provided coordinates'''
    board = [[0 for i in range(board_diamensions['x'])] for i in range(board_diamensions['y'])]
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            if (row, column) in alive_coords_to_start:
                board[row][column] = 1
            else:
                board[row][column] = 0
    return board
    
def read_coords_file(file):
    print('x')
    with open(file, 'r') as f:
        raw = f.readline() # should all be on 1 line
        print(raw)
    coords_dirty = [coord for coord in raw.split(',')]
    coords = []
    print(coords_dirty)
    #for coord in coords_dirty # make this all work
    return coords
    
def get_neighbour_count(board,row,column): # This needs the board as a parameter else it does the default one 
    '''Returns the number of adjacent alive cells# to the cell with coordinates provided'''
    neighbour_count = 0
    for y in range(column-1, column+2):
        # Iterate over the x range
        for x in range(row-1, row+2): # these might be the other way round
            try:
                if board[x][y] == 1:
                    neighbour_count += 1 
            except:
                pass # imagine all non existant cells are dead
    return neighbour_count 
    
def run(board: list, board_diamensions: dict):
    'Recursively runs one iteration of the game, checking to see if cells are alive and modifying itself accordingly'
    time.sleep(1)

    board = list(board)
    new_board = copy.deepcopy(board)
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            neighbour_count = get_neighbour_count(board,row,column)
            
            #for live cells
            if board[row][column] == 1:
                neighbour_count -= 1 # omg idk why but it finally works it was checking itself IT WOKS
                if neighbour_count < 2 or neighbour_count > 3:
                    new_board[row][column] = 0
                    #print(f'cell at {row},{column} died due to {neighbour_count} neighbours')
                elif neighbour_count == 2 or neighbour_count == 3:
                    new_board[row][column] = 1
                    #print(f'cell at {row},{column} survived due to {neighbour_count} neighbours')
            # for dead cells
            if board[row][column] == 0:
                if neighbour_count == 3:
                    new_board[row][column] = 1
                    #print(f'cell at {row},{column} revived due to {neighbour_count} neighbours')
    
    pprint.pp(new_board)

    run(new_board)
        


if __name__ == '__main__':
    main()