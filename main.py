import time
import copy
import random
import argparse
import os

# use file reading to give examples of interesting starting coords to user 




# add requests scraping from the website to generate new files and set the rest as gitignores so its a cleaner repo but on startup it downloads them all>
# allow user to select colour scheme  - affect starting message?

# add a way to get a random interesting structure from wiki
"""
for row in colour_board:
            print("  ".join(row))
this is adapted from online
"""

def print_board(board: list) -> None:
    """Prints the current state of the board aesthetically"""
    # NOTE: This does not work on IDLE as it does not use a real terminal.
    WHITE = "\u001b[33m#\u001b[0m"
    BLACK = "\u001b[31m#\u001b[0m"
    colour_board = copy.deepcopy(board)
    for row in range(len(board)):
        for column in range(len(board[row])):
            colour_board[row][column] = WHITE if board[row][column] == 1 else BLACK
    for row in colour_board:
        print("  ".join(row))


def parse_args() -> tuple[str, dict, float]:
    """Parses the arguments to provide key metadata for simulation"""
    parser = argparse.ArgumentParser(
    prog="main.py",
    description="A numerical simulation of Conway's Game of Life",
    usage=f"python3 main.py [-h] [-w WIDTH] [-e ELEVATION] [-f FILENAME] [-d DELAY] [-r RANDOM]"
)
    parser.add_argument('-w', '--width', help='width in squares of board, default is 40, some diamensions may break patterns')
    parser.add_argument('-e', '--elevation', help='height in squares of board, default is 40, some diamensions may break patterns')
    parser.add_argument('-f', '--filename', help="path to file with starting coordinates, default is coords/coords.txt")
    parser.add_argument('-d', '--delay', help="time between generations")
    parser.add_argument('-r', '--random', help="random start or not (y/n)")
    # Yes I am aware that elevation is a stupid name for height but I'm already using the -h flag for help

    args = parser.parse_args()
    print(args)
    board_diamensions = {
        'x': int(args.width) if args.width != None else 40,
        'y': int(args.elevation) if args.elevation != None else 40
    }
    args.filename = "coords.txt" if args.filename == None else args.filename
    args.delay = float(args.delay) if args.delay != None else 1
    args.random = True if args.random.lower() == 'y' else False
    return f'coords/{args.filename}', board_diamensions, args.delay, args.random


def check_empty_file(file: str) -> None:
    """Checks if the provided coordinate file is empty and crashes if so"""
    with open(file, "r") as f:
        raw = f.readlines()
    for line in raw:
        if line != '':
            return False
    print("""
        \u001b[31mCause of crash: `{file}` is empty.\u001b[0m
              """)
    quit()


def introduction(file: str) -> None:
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
          before running this program
          or use a preset file
          """)
    check_empty_file(file) # make sure this works with the presets
    time.sleep(2)
    os.system('clear')
        

def fetch_starting_coords(file: str, random:bool, board_diamensions:dict) -> list:
    """Fetches coords from input file"""
    if random:
        return noise_generator(board_diamensions)
    with open(file, "r") as f:
        raw = f.readlines()
    pattern = False
    for line in range(len(raw)): # Check if it is a pattern or coordsheet
        if '.' in raw[line]:
            pattern = True
    
    if not pattern:
        coords = fetch_coords_from_coords(raw)
    elif pattern:
        coords = fetch_coords_from_pattern(raw)
    else:
        coords = fetch_coords_from_coords(raw)
    return coords


def noise_generator(board_diamensions:dict) -> list:
    board = [[random.randrange(0,2) for y in range(board_diamensions['y'])] for x in range(board_diamensions['x'])]
    print(board)
    coords = []
    for row in range(len(board)):
        indicies  = [index for (index, item) in enumerate(board[row]) if item == 1] # Adapted from https://www.freecodecamp.org/news/python-find-in-list-how-to-find-the-index-of-an-item-or-element-in-a-list/
        for index in indicies:
            coords.append(tuple((row, index)))
    return coords
    

def fetch_coords_from_coords(raw:list) -> list:
    coords = []
    for line in raw:
        coords.append(tuple(int(x) for x in line.strip(' ').split(',')))
    return coords


def fetch_coords_from_pattern(raw:list):
    coords = []
    pattern = copy.deepcopy(raw)
    
    for line in range(len(raw)): # removes starting info
        if raw[line][0] == '!':
            pattern.remove(raw[line])
    for row in range(len(pattern)):
        print(pattern[row])
        indicies  = [index for (index, item) in enumerate(pattern[row]) if item == "O"] # Adapted from https://www.freecodecamp.org/news/python-find-in-list-how-to-find-the-index-of-an-item-or-element-in-a-list/
        for index in indicies:
            coords.append(tuple((row, index)))
    return coords

def generate_starting_board(alive_coords_to_start: list, board_diamensions: dict) -> list:
    '''Generates a board of provided size with alive cells at provided coordinates'''
    board = [[0 for i in range(board_diamensions['x'])] for j in range(board_diamensions['y'])] # were botjh i, changfed to i,j but thismany be a mistake
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            if (row, column) in alive_coords_to_start:
                board[row][column] = 1
            else:
                board[row][column] = 0
    return board


def get_neighbour_count(board: list, row: int, column: int) -> int:
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


def run(board: list, board_diamensions: dict, delay: float):
    '''Recursively runs one iteration of the game, checking to see if cells are alive and modifying itself accordingly'''
    time.sleep(delay)
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
        

    run(new_board, board_diamensions, delay)


def main():
    file, board_diamensions, delay, random = parse_args()
    introduction(file)
    alive_coords_to_start = fetch_starting_coords(file, random, board_diamensions)
    board = generate_starting_board(alive_coords_to_start,board_diamensions)
    run(board, board_diamensions, delay)

if __name__ == '__main__':
    main()