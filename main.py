import numpy as np
import pprint
import time
import copy
# use file reading to give examples of interesting starting coords to user 

# add an option for random noise start
board_diamensions = {
    'x': 8,
    'y': 10
}


def main():
    start()
    alive_coords_to_start = fetch_starting_coords()
    board = generate_starting_board(alive_coords_to_start)
    pprint.pp(board)
    run(board)


def start():
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
    presets = print("""
        If you want to run a preset example setup, type the corresponding name:
            glider: 
            none: Enter your own starting coordinates
          """)
    check_empty() # make sure this works with the presets
    # allow to decide diamenisons 
        



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


def fetch_starting_coords():
    with open("coords.txt", "r") as f:
        raw = f.readlines()
    coords = []
    for line in raw:
        coords.append(tuple(int(x) for x in line.split(',')))
    print(coords)
    return coords

def generate_starting_board(alive_coords_to_start: list):
    '''Generates a board of provided size with alive cells at provided coordinates'''
    board = [[0 for i in range(board_diamensions['x'])] for i in range(board_diamensions['y'])]
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            if (row, column) in alive_coords_to_start:
                board[row][column] = 1
            else:
                board[row][column] = 0
    return board

def get_neighbour_count(board,row,column): # This needs the board as a parameter else it does the default one 
    '''Returns the number of adjacent alive cells to the cell with coordinates provided'''
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
    
def run(board: list):
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