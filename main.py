# make display graphically though like ths behind the scenes
import numpy as np
import pprint
import time
import copy

# work through this in vscode with a proper debugger
'''
Any live cell with fewer than two live neighbours dies, as if by underpopulation.

Any live cell with two or three live neighbours lives on to the next generation.

Any live cell with more than three live neighbours dies, as if by overpopulation.

Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
'''
# add an option for random noise start
board_diamensions = {
    'x': 8,
    'y': 10
}
alive_coords_to_start = [(3,2),(3,3),(3,4)]
def main():
    board = generate_starting_board()
    pprint.pp(board)
    run(board) # let user choose num2
    #do this recursively

def generate_starting_board():
    board = [[0 for i in range(board_diamensions['x'])] for i in range(board_diamensions['y'])]
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            if (row, column) in alive_coords_to_start:
                board[row][column] = 1
            else:
                board[row][column] = 0
    return board

def check_if_all_dead(board) -> bool:
    alive = False
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            if board[row][column] == 1:
                alive = True
    return alive
    
def run(board: list):
    ''' FIX ALGORITHM AS CHECKING FOR DEAD CELL DEOSNT WORK PERFECTLY AND TIMESLEEP DOESNT WORK AFTER FIRST RECURSION'''
    time.sleep(2)

    board = list(board)
    all_cell_neighbour_counts = {
        (range(board_diamensions['x']),range(board_diamensions['y'])): 'neighbour_count'
    }
    all_cell_neighbour_counts = {}
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            all_cell_neighbour_counts.update({(row,column):None})
    adjacent_coords = [ # check if diagonals count
        (+1, 0),
        (-1, 0),
        (0, +1),
        (0,-1),
        (+1,+1),
        (-1,+1),
        (+1,- 1),
        (-1,- 1)
    ]
    '''
    adjacent_coords = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x + 1, y - 1),
        (x - 1, y - 1)
    ]

    neighbour_count = [n for n in all_nodes if n.coords in adjacent_coords]
    
    
    '''

    new_board = copy.deepcopy(board)
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            #neighbour_count = all_cell_neighbour_counts.get((row, column))
            # just do neighbour count check here instead of own section - bastract into a function later
            neighbour_count = 0
            for y in range(column-1, column+2):
                # Iterate over the x range
                for x in range(row-1, row+2): # these might be the other way round
                    try:
                        if board[x][y] == 1:
                            neighbour_count += 1 
                    except:
                        pass # imagine all non existant cells are dead
                    
            #print(neighbour_count)
            #for live cells
            if board[row][column] == 1:
                neighbour_count -= 1 # omg idk why but it finally works it was checking itself IT WOKS
                if neighbour_count < 2 or neighbour_count > 3:
                    new_board[row][column] = 0
                    print(f'cell at {row},{column} died due to {neighbour_count} neighbours')
                elif neighbour_count == 2 or neighbour_count == 3:
                    new_board[row][column] = 1
                    print(f'cell at {row},{column} survived due to {neighbour_count} neighbours')
            # for dead cells
            if board[row][column] == 0:
                if neighbour_count == 3:
                    new_board[row][column] = 1
                    print(f'cell at {row},{column} revived due to {neighbour_count} neighbours')
    
    # check if 0-index errors
    pprint.pp(new_board)
    #all_dead: bool = check_if_all_dead(new_board)
    #if all_dead:
    #    pprint.pp([[0 for col in range(board_diamensions['x'])] for row in range(board_diamensions['y'])])
    #    quit()

    run(new_board)
        


    # make it stop if all cells dead
if __name__ == '__main__':
    main()